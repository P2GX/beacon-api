"""Tests for Beacon v2 filter parsing functionality."""

import pytest

from beacon_api.api.query_params import parse_filters_from_string


class TestJSONFilterParsing:
    """Test JSON format filter parsing (POST requests)."""

    def test_single_ontology_filter_json(self):
        """Test parsing a single ontology filter from JSON."""
        result = parse_filters_from_string('[{"id":"HP:0001250"}]')
        assert len(result) == 1
        assert result[0].id == "HP:0001250"
        assert result[0].operator is None
        assert result[0].value is None

    def test_multiple_ontology_filters_json(self):
        """Test parsing multiple ontology filters from JSON."""
        result = parse_filters_from_string('[{"id":"HP:0001250"},{"id":"NCIT:C6975"}]')
        assert len(result) == 2
        assert result[0].id == "HP:0001250"
        assert result[1].id == "NCIT:C6975"

    def test_alphanumeric_filter_json(self):
        """Test parsing alphanumeric filter with operator and value."""
        result = parse_filters_from_string(
            '[{"id":"PATO:0000011","operator":">","value":"P70Y"}]'
        )
        assert len(result) == 1
        assert result[0].id == "PATO:0000011"
        assert result[0].operator == ">"
        assert result[0].value == "P70Y"

    def test_numeric_filter_json(self):
        """Test parsing numeric filter with integer value."""
        result = parse_filters_from_string('[{"id":"age","operator":">=","value":18}]')
        assert len(result) == 1
        assert result[0].id == "age"
        assert result[0].operator == ">="
        assert result[0].value == 18

    def test_mixed_filters_json(self):
        """Test parsing mix of ontology and alphanumeric filters."""
        result = parse_filters_from_string(
            '[{"id":"HP:0001250"},{"id":"PATO:0000011","operator":">","value":"P70Y"}]'
        )
        assert len(result) == 2
        assert result[0].id == "HP:0001250"
        assert result[0].operator is None
        assert result[1].id == "PATO:0000011"
        assert result[1].operator == ">"
        assert result[1].value == "P70Y"

    def test_filter_with_include_descendant_terms(self):
        """Test parsing filter with includeDescendantTerms."""
        result = parse_filters_from_string(
            '[{"id":"HP:0001250","includeDescendantTerms":false}]'
        )
        assert len(result) == 1
        assert result[0].id == "HP:0001250"
        assert result[0].includeDescendantTerms is False

    def test_filter_with_similarity(self):
        """Test parsing filter with similarity parameter."""
        result = parse_filters_from_string('[{"id":"HP:0001250","similarity":"high"}]')
        assert len(result) == 1
        assert result[0].id == "HP:0001250"
        assert result[0].similarity == "high"


class TestCommaSeparatedFilterParsing:
    """Test comma-separated format filter parsing (GET requests)."""

    def test_single_ontology_filter_comma(self):
        """Test parsing single ontology filter."""
        result = parse_filters_from_string("HP:0001250")
        assert len(result) == 1
        assert result[0].id == "HP:0001250"
        assert result[0].operator is None

    def test_multiple_ontology_filters_comma(self):
        """Test parsing multiple comma-separated ontology filters."""
        result = parse_filters_from_string("HP:0001250,NCIT:C6975,HP:0100526")
        assert len(result) == 3
        assert result[0].id == "HP:0001250"
        assert result[1].id == "NCIT:C6975"
        assert result[2].id == "HP:0100526"

    def test_ontology_filter_with_underscore(self):
        """Test parsing filter with underscore instead of colon."""
        result = parse_filters_from_string("PATO_0000011")
        assert len(result) == 1
        assert result[0].id == "PATO:0000011"  # Underscore converted to colon

    def test_alphanumeric_filter_greater_than(self):
        """Test parsing alphanumeric filter with > operator."""
        result = parse_filters_from_string("PATO_0000011:>P70Y")
        assert len(result) == 1
        assert result[0].id == "PATO:0000011"
        assert result[0].operator == ">"
        assert result[0].value == "P70Y"

    def test_alphanumeric_filter_equals(self):
        """Test parsing alphanumeric filter with = operator."""
        result = parse_filters_from_string("variant_type:=SNP")
        assert len(result) == 1
        assert result[0].id == "variant:type"  # Underscore converted
        assert result[0].operator == "="
        assert result[0].value == "SNP"

    def test_numeric_filter_greater_than_equals(self):
        """Test parsing numeric filter with >= operator."""
        result = parse_filters_from_string("age:>=18")
        assert len(result) == 1
        assert result[0].id == "age"
        assert result[0].operator == ">="
        assert result[0].value == 18
        assert isinstance(result[0].value, int)

    def test_numeric_filter_float_value(self):
        """Test parsing numeric filter with float value."""
        result = parse_filters_from_string("score:>3.5")
        assert len(result) == 1
        assert result[0].id == "score"
        assert result[0].operator == ">"
        assert result[0].value == 3.5
        assert isinstance(result[0].value, float)

    def test_mixed_filters_comma_separated(self):
        """Test parsing mix of ontology and alphanumeric filters."""
        result = parse_filters_from_string("NCIT:C6975,PATO_0000011:>P70Y,HP:0001250")
        assert len(result) == 3
        assert result[0].id == "NCIT:C6975"
        assert result[0].operator is None
        assert result[1].id == "PATO:0000011"
        assert result[1].operator == ">"
        assert result[1].value == "P70Y"
        assert result[2].id == "HP:0001250"
        assert result[2].operator is None

    def test_filter_with_not_operator(self):
        """Test parsing filter with ! (NOT) operator."""
        result = parse_filters_from_string("status:!active")
        assert len(result) == 1
        assert result[0].id == "status"
        assert result[0].operator == "!"
        assert result[0].value == "active"

    def test_filter_with_less_than(self):
        """Test parsing filter with < operator."""
        result = parse_filters_from_string("age:<65")
        assert len(result) == 1
        assert result[0].id == "age"
        assert result[0].operator == "<"
        assert result[0].value == 65


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_filter_string(self):
        """Test parsing empty filter string returns None."""
        result = parse_filters_from_string("")
        assert result is None

    def test_none_filter_string(self):
        """Test parsing None filter string returns None."""
        result = parse_filters_from_string(None)
        assert result is None

    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises ValueError."""
        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_filters_from_string('[{"id":"HP:0001250"')

    def test_json_non_dict_array_raises_error(self):
        """Test that JSON array of non-dicts raises ValueError."""
        with pytest.raises(ValueError, match="Invalid filter format"):
            parse_filters_from_string('["string1", "string2"]')

    def test_whitespace_handling_comma_separated(self):
        """Test that whitespace around commas is handled correctly."""
        result = parse_filters_from_string("HP:0001250 , NCIT:C6975 , HP:0100526")
        assert len(result) == 3
        assert result[0].id == "HP:0001250"
        assert result[1].id == "NCIT:C6975"
        assert result[2].id == "HP:0100526"

    def test_empty_comma_segments_ignored(self):
        """Test that empty segments between commas are ignored."""
        result = parse_filters_from_string("HP:0001250,,NCIT:C6975")
        assert len(result) == 2
        assert result[0].id == "HP:0001250"
        assert result[1].id == "NCIT:C6975"


class TestBeaconV2Examples:
    """Test examples from Beacon v2 specification."""

    def test_beacon_v2_ontology_example(self):
        """Test ontology filter example from spec."""
        result = parse_filters_from_string('[{"id":"HP:0100526"}]')
        assert len(result) == 1
        assert result[0].id == "HP:0100526"

    def test_beacon_v2_alphanumeric_example(self):
        """Test alphanumeric filter example from spec."""
        result = parse_filters_from_string(
            '[{"id":"PATO:0000011","operator":">","value":"P70Y"}]'
        )
        assert len(result) == 1
        assert result[0].id == "PATO:0000011"
        assert result[0].operator == ">"
        assert result[0].value == "P70Y"

    def test_beacon_v2_multiple_filters_example(self):
        """Test multiple filters example from spec."""
        result = parse_filters_from_string(
            '[{"id":"NCIT:C6975"},{"id":"PATO:0000011","operator":">","value":"P70Y"}]'
        )
        assert len(result) == 2
        assert result[0].id == "NCIT:C6975"
        assert result[1].id == "PATO:0000011"
        assert result[1].operator == ">"
        assert result[1].value == "P70Y"

    def test_beacon_v2_get_format_simple(self):
        """Test GET format simple filters from spec."""
        result = parse_filters_from_string("PMID:22824167,NCIT:C6975")
        assert len(result) == 2
        assert result[0].id == "PMID:22824167"
        assert result[1].id == "NCIT:C6975"

    def test_beacon_v2_get_format_with_operator(self):
        """Test GET format with operator from spec."""
        result = parse_filters_from_string("PATO_0000011:>P70Y")
        assert len(result) == 1
        assert result[0].id == "PATO:0000011"
        assert result[0].operator == ">"
        assert result[0].value == "P70Y"
