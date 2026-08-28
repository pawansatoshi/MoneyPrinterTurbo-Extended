import json
import importlib
import sys
import types


def test_script_writer_handles_chat_template_batch_encoding(tmp_path, monkeypatch):
    research = tmp_path / "research.json"
    out = tmp_path / "script.txt"
    research.write_text(
        json.dumps([{"title": "Title", "headings": ["Heading"], "paragraphs": ["Fact paragraph " * 5]}]),
        encoding="utf-8",
    )

    class FakeTensor:
        shape = (1, 3)

    class FakeBatch:
        input_ids = FakeTensor()

    class FakeTokenizer:
        def apply_chat_template(self, *args, **kwargs):
            return FakeBatch()

        def decode(self, *args, **kwargs):
            return "Generated narration."

    class FakeModel:
        def generate(self, *, input_ids, **kwargs):
            assert input_ids is FakeBatch.input_ids
            return [[100, 101, 102, 103, 104]]

    class FakeAutoTokenizer:
        @staticmethod
        def from_pretrained(*args, **kwargs):
            return FakeTokenizer()

    class FakeAutoModel:
        @staticmethod
        def from_pretrained(*args, **kwargs):
            return FakeModel()

    fake_transformers = types.ModuleType("transformers")
    fake_transformers.AutoTokenizer = FakeAutoTokenizer
    fake_transformers.AutoModelForCausalLM = FakeAutoModel
    monkeypatch.setitem(sys.modules, "transformers", fake_transformers)
    sys.modules.pop("studio.production.script_writer", None)
    script_writer = importlib.import_module("studio.production.script_writer")
    monkeypatch.setattr(sys, "argv", ["script_writer.py", str(research), "English", str(out), "60"])

    script_writer.main()

    assert out.read_text(encoding="utf-8") == "Generated narration."
