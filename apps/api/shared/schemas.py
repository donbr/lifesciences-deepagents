"""
Pydantic schemas for knowledge graph validation.

Enforces consistent structure for graph artifacts emitted by the persistence_specialist.
Every run must produce validated graph.json + report.md regardless of external service availability.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Any, Literal, Optional
from datetime import datetime, timezone


# Valid CURIE prefixes for life sciences entities
VALID_CURIE_PREFIXES = {
    "HGNC",      # Gene symbols
    "UniProtKB", # Proteins
    "CHEMBL",    # ChEMBL compounds
    "PUBCHEM",   # PubChem compounds
    "MONDO",     # Disease ontology
    "NCIt",      # NCI Thesaurus
    "ENSG",      # Ensembl genes
    "ENSP",      # Ensembl proteins
    "NCT",       # ClinicalTrials.gov
}


class GraphNode(BaseModel):
    """
    Represents a biological entity in the knowledge graph.

    All node IDs MUST use full CURIE format for graph persistence.
    Example: "HGNC:171" not "171", "UniProtKB:Q04771" not "Q04771"
    """
    id: str = Field(
        ...,
        description="Full CURIE identifier (e.g., 'HGNC:171', 'CHEMBL:3137309')"
    )
    type: Literal["Gene", "Protein", "Compound", "Drug", "Disease", "Pathway", "Trial", "Variant"] = Field(
        ...,
        description="Entity type from controlled vocabulary"
    )
    label: str = Field(
        ...,
        description="Human-readable name (e.g., 'ACVR1', 'Venetoclax')"
    )
    properties: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (ensembl_id, uniprot_id, mechanism, phase, etc.)"
    )

    @field_validator('id')
    @classmethod
    def validate_curie_format(cls, v: str) -> str:
        """Validate CURIE format: PREFIX:ID"""
        if ':' not in v:
            raise ValueError(
                f"Node ID must be full CURIE format (PREFIX:ID), got: {v}. "
                f"Example: 'HGNC:171' not '171'"
            )

        prefix = v.split(':')[0]
        if prefix not in VALID_CURIE_PREFIXES:
            # Log warning but don't fail - allows extensibility
            pass

        return v

    @field_validator('label')
    @classmethod
    def validate_label_not_empty(cls, v: str) -> str:
        """Ensure label is not empty"""
        if not v or not v.strip():
            raise ValueError("Node label cannot be empty")
        return v.strip()


class GraphEdge(BaseModel):
    """
    Represents a relationship between two entities.

    All edges MUST have:
    - Valid source/target CURIEs (must match node IDs)
    - Relationship type from controlled vocabulary
    - Evidence list with tool call references
    """
    source: str = Field(
        ...,
        description="Source node CURIE (must exist in nodes list)"
    )
    target: str = Field(
        ...,
        description="Target node CURIE (must exist in nodes list)"
    )
    type: str = Field(
        ...,
        description="Relationship type (REGULATES, INHIBITS, TARGETS, ASSOCIATES_WITH, etc.)"
    )
    properties: dict[str, Any] = Field(
        default_factory=dict,
        description="Edge metadata (mechanism, confidence, evidence sources)"
    )
    evidence: list[str] = Field(
        default_factory=list,
        description="Tool call references supporting this edge (e.g., ['uniprot_get_protein(P04637)', 'string_get_interactions(P04637)'])"
    )

    @field_validator('source', 'target')
    @classmethod
    def validate_curie_format(cls, v: str) -> str:
        """Validate source/target are CURIEs"""
        if ':' not in v:
            raise ValueError(
                f"Edge source/target must be full CURIE format, got: {v}"
            )
        return v

    @field_validator('type')
    @classmethod
    def validate_relationship_type(cls, v: str) -> str:
        """Ensure relationship type is uppercase and non-empty"""
        if not v or not v.strip():
            raise ValueError("Edge type cannot be empty")
        # Convert to uppercase convention for graph databases
        return v.strip().upper()


class KnowledgeGraph(BaseModel):
    """
    Complete validated knowledge graph structure.

    This is the primary artifact emitted by the persistence_specialist.
    MUST be written to /graph.json on every run.
    """
    nodes: list[GraphNode] = Field(
        default_factory=list,
        description="List of entities in the graph"
    )
    edges: list[GraphEdge] = Field(
        default_factory=list,
        description="List of relationships between entities"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Graph-level metadata (query, timestamp, phase results, etc.)"
    )

    @model_validator(mode='after')
    def validate_edge_references(self):
        """Ensure all edge source/target CURIEs exist in nodes list"""
        node_ids = {node.id for node in self.nodes}

        for i, edge in enumerate(self.edges):
            if edge.source not in node_ids:
                raise ValueError(
                    f"Edge {i} references non-existent source node: {edge.source}. "
                    f"Available node IDs: {sorted(node_ids)}"
                )
            if edge.target not in node_ids:
                raise ValueError(
                    f"Edge {i} references non-existent target node: {edge.target}. "
                    f"Available node IDs: {sorted(node_ids)}"
                )

        return self

    @model_validator(mode='after')
    def validate_minimum_content(self):
        """Warn if graph is empty (allowed but suspicious)"""
        if not self.nodes and not self.edges:
            # Don't fail - empty graphs are valid for "no results" cases
            pass
        return self

    def to_graphiti_format(self) -> dict[str, Any]:
        """
        Convert to Graphiti episode format for persist_to_graphiti tool.

        Returns:
            Dict with nodes/edges/metadata ready for JSON serialization
        """
        return {
            "nodes": [node.model_dump() for node in self.nodes],
            "edges": [edge.model_dump() for edge in self.edges],
            "metadata": {
                **self.metadata,
                "created_by": "lifesciences-agent",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "schema_version": "1.0"
            }
        }

    def summary_stats(self) -> dict[str, Any]:
        """Generate summary statistics for logging/reporting"""
        entity_types: dict[str, int] = {}
        for node in self.nodes:
            entity_types[node.type] = entity_types.get(node.type, 0) + 1

        relationship_types: dict[str, int] = {}
        for edge in self.edges:
            relationship_types[edge.type] = relationship_types.get(edge.type, 0) + 1

        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "entity_types": entity_types,
            "relationship_types": relationship_types
        }


def validate_knowledge_graph(graph_data: dict[str, Any]) -> tuple[bool, Optional[KnowledgeGraph], Optional[str]]:
    """
    Validate knowledge graph data against schema.

    Args:
        graph_data: Raw dict with nodes/edges/metadata

    Returns:
        Tuple of (is_valid, validated_graph, error_message)
        - If valid: (True, KnowledgeGraph, None)
        - If invalid: (False, None, error_message)

    Example:
        is_valid, graph, error = validate_knowledge_graph(raw_data)
        if not is_valid:
            print(f"Validation failed: {error}")
            # Request retry from specialist
        else:
            # Write graph.model_dump_json() to /graph.json
    """
    try:
        graph = KnowledgeGraph(**graph_data)
        return True, graph, None
    except Exception as e:
        error_msg = f"Knowledge graph validation failed: {str(e)}"
        return False, None, error_msg


def create_empty_graph(reason: str = "No results found") -> KnowledgeGraph:
    """
    Create a valid empty knowledge graph for failure cases.

    Use when upstream phases fail but we still need to emit artifacts.

    Args:
        reason: Human-readable explanation for empty graph

    Returns:
        Valid KnowledgeGraph with empty nodes/edges
    """
    return KnowledgeGraph(
        nodes=[],
        edges=[],
        metadata={
            "status": "empty",
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )
