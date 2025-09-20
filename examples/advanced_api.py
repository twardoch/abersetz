#!/usr/bin/env python3
# this_file: examples/advanced_api.py

"""Advanced examples demonstrating sophisticated abersetz usage."""

import asyncio
import json
from pathlib import Path

from abersetz import TranslationResult, TranslatorOptions, translate_path
from abersetz.config import AbersetzConfig, load_config
from abersetz.engines import EngineRequest, create_engine


class TranslationWorkflow:
    """Advanced translation workflow with progress tracking."""

    def __init__(self, config: AbersetzConfig = None):
        self.config = config or load_config()
        self.results: list[TranslationResult] = []
        self.errors: dict[str, str] = {}

    def translate_project(
        self, source_dir: str, target_langs: list[str], engine: str = "translators/google"
    ):
        """Translate entire project to multiple languages."""
        source_path = Path(source_dir)

        for lang in target_langs:
            print(f"\n=== Translating to {lang} ===")
            output_dir = source_path.parent / f"{source_path.name}_{lang}"

            try:
                lang_results = translate_path(
                    str(source_path),
                    TranslatorOptions(
                        to_lang=lang,
                        engine=engine,
                        output_dir=output_dir,
                        recurse=True,
                        include=("*.md", "*.txt", "*.html"),
                        exclude=("*test*", "*draft*", ".*"),
                    ),
                    config=self.config,
                )
                self.results.extend(lang_results)
                print(f"✓ {lang}: {len(lang_results)} files translated")

            except Exception as e:
                self.errors[lang] = str(e)
                print(f"✗ {lang}: Failed - {e}")

    def generate_report(self, output_file: str = "translation_report.json"):
        """Generate detailed translation report."""
        report = {
            "total_files": len(self.results),
            "total_chunks": sum(r.chunks for r in self.results),
            "languages": {},
            "errors": self.errors,
            "files": [],
        }

        # Group by language
        for result in self.results:
            lang = result.destination.parent.name.split("_")[-1]
            if lang not in report["languages"]:
                report["languages"][lang] = {"files": 0, "chunks": 0, "formats": {}}

            report["languages"][lang]["files"] += 1
            report["languages"][lang]["chunks"] += result.chunks

            fmt = result.format.value
            if fmt not in report["languages"][lang]["formats"]:
                report["languages"][lang]["formats"][fmt] = 0
            report["languages"][lang]["formats"][fmt] += 1

            report["files"].append(
                {
                    "source": str(result.source),
                    "destination": str(result.destination),
                    "chunks": result.chunks,
                    "format": result.format.value,
                    "vocabulary_size": len(result.vocabulary),
                }
            )

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\nReport saved to {output_file}")
        return report


class VocabularyManager:
    """Manage translation vocabularies across projects."""

    def __init__(self):
        self.vocabularies: dict[str, dict[str, str]] = {}

    def load_vocabulary(self, file_path: str, lang_pair: str):
        """Load vocabulary from JSON file."""
        with open(file_path) as f:
            self.vocabularies[lang_pair] = json.load(f)

    def merge_vocabularies(self, *lang_pairs: str) -> dict[str, str]:
        """Merge multiple vocabularies."""
        merged = {}
        for pair in lang_pairs:
            if pair in self.vocabularies:
                merged.update(self.vocabularies[pair])
        return merged

    def translate_with_consistency(
        self, files: list[str], to_lang: str, base_vocabulary: dict[str, str] = None
    ):
        """Translate files with consistent terminology."""
        accumulated_vocab = base_vocabulary or {}
        results = []

        for file_path in files:
            print(f"Translating {file_path} with {len(accumulated_vocab)} terms...")

            file_results = translate_path(
                file_path,
                TranslatorOptions(
                    to_lang=to_lang,
                    engine="ullm/default",  # LLM engine for vocabulary support
                    initial_vocabulary=accumulated_vocab,
                    save_vocabulary=True,
                ),
            )

            if file_results:
                result = file_results[0]
                results.append(result)
                # Update accumulated vocabulary
                accumulated_vocab.update(result.vocabulary)
                print(f"  Added {len(result.vocabulary)} new terms")

        return results, accumulated_vocab


class ParallelTranslator:
    """Translate using multiple engines in parallel for comparison."""

    async def translate_with_engine(self, text: str, engine_name: str, to_lang: str):
        """Async translation with a specific engine."""
        config = load_config()
        engine = create_engine(engine_name, config)

        request = EngineRequest(
            text=text,
            source_lang="auto",
            target_lang=to_lang,
            is_html=False,
            vocabulary={},
            prolog={},
            chunk_index=0,
            total_chunks=1,
        )

        try:
            result = engine.translate(request)
            return engine_name, result.text
        except Exception as e:
            return engine_name, f"Error: {e}"

    async def compare_translations(self, text: str, engines: list[str], to_lang: str):
        """Compare translations from multiple engines."""
        tasks = [self.translate_with_engine(text, engine, to_lang) for engine in engines]
        results = await asyncio.gather(*tasks)

        print("\n=== Translation Comparison ===")
        print(f"Original: {text[:100]}...")
        print(f"Target language: {to_lang}\n")

        for engine_name, translation in results:
            print(f"{engine_name}:")
            print(f"  {translation[:200]}")
            print()

        return dict(results)


# Example usage functions
def example_multi_language():
    """Translate documentation to multiple languages."""
    workflow = TranslationWorkflow()
    workflow.translate_project(
        source_dir="docs",
        target_langs=["es", "fr", "de", "ja", "zh-CN"],
        engine="translators/google",
    )
    workflow.generate_report()


def example_vocabulary_consistency():
    """Maintain consistent terminology across documents."""
    manager = VocabularyManager()

    # Load existing vocabulary
    technical_terms = {
        "API": "API",
        "endpoint": "endpoint",
        "webhook": "webhook",
        "pipeline": "pipeline de procesamiento",
    }

    files = ["api_reference.md", "user_guide.md", "developer_docs.md"]

    results, final_vocab = manager.translate_with_consistency(
        files=files, to_lang="es", base_vocabulary=technical_terms
    )

    # Save final vocabulary
    with open("technical_vocabulary_es.json", "w") as f:
        json.dump(final_vocab, f, indent=2, ensure_ascii=False)

    print(f"\nFinal vocabulary has {len(final_vocab)} terms")


def example_parallel_comparison():
    """Compare translations from different engines."""
    translator = ParallelTranslator()

    text = """
    Artificial intelligence is transforming how we interact with technology.
    Machine learning models can now understand context, generate creative content,
    and solve complex problems that were once thought to require human intelligence.
    """

    engines = [
        "translators/google",
        "translators/bing",
        "deep-translator/google",
        "hysf",  # Requires API key
    ]

    # Run async comparison
    asyncio.run(translator.compare_translations(text, engines, "fr"))


def example_incremental_translation():
    """Translate large projects incrementally."""

    class IncrementalTranslator:
        def __init__(self, checkpoint_file: str = ".translation_checkpoint.json"):
            self.checkpoint_file = checkpoint_file
            self.completed = self.load_checkpoint()

        def load_checkpoint(self) -> set:
            if Path(self.checkpoint_file).exists():
                with open(self.checkpoint_file) as f:
                    return set(json.load(f))
            return set()

        def save_checkpoint(self):
            with open(self.checkpoint_file, "w") as f:
                json.dump(list(self.completed), f)

        def translate_incrementally(self, source_dir: str, to_lang: str):
            all_files = Path(source_dir).rglob("*.md")
            pending = [f for f in all_files if str(f) not in self.completed]

            print(f"Found {len(pending)} files to translate")
            print(f"Already completed: {len(self.completed)} files")

            for file_path in pending:
                try:
                    print(f"Translating {file_path}...")
                    results = translate_path(str(file_path), TranslatorOptions(to_lang=to_lang))
                    if results:
                        self.completed.add(str(file_path))
                        self.save_checkpoint()
                        print(f"  ✓ Saved to {results[0].destination}")
                except Exception as e:
                    print(f"  ✗ Failed: {e}")
                    # Continue with next file

            print("\nTranslation complete!")
            print(f"Total files processed: {len(self.completed)}")

    translator = IncrementalTranslator()
    translator.translate_incrementally("large_docs/", "es")


if __name__ == "__main__":
    import sys

    examples = {
        "multi": example_multi_language,
        "vocab": example_vocabulary_consistency,
        "compare": example_parallel_comparison,
        "incremental": example_incremental_translation,
    }

    if len(sys.argv) > 1 and sys.argv[1] in examples:
        examples[sys.argv[1]]()
    else:
        print(f"Usage: {sys.argv[0]} {{{','.join(examples.keys())}}}")
        print("\nAdvanced examples:")
        for name, func in examples.items():
            print(f"  {name}: {func.__doc__.strip()}")
