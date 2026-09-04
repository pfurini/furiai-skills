# Common fixture assets

Shared fixture factories live in `../../conftest.py` and write all generated skills, campaigns, JSONL transcripts, and subprocess results below pytest's isolated temporary directory. Order-specific static fixture data belongs in a sibling directory owned by that order.
