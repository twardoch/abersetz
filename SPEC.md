---
this_file: SPEC.md
---
# Abersetz Technical Specification

## 1. Overview

`abersetz` is a Python package and command-line tool for translating the content of files. It operates on a pipeline of locating files, chunking their content, translating the chunks, and merging them back into translated files.

## 2. Core Functionality

### 2.1. File Handling

-   **Input:** The tool shall accept a path to a single file or a directory.
-   **File Discovery:** When given a directory, the tool shall be able to recursively find files to translate. A `--recurse` flag should control this behavior.
-   **Output:** The tool shall support two output modes:
    -   Saving translated files to a specified output directory, mirroring the source directory structure.
    -   Overwriting the original files with their translated content, using an `--write_over` flag.

### 2.2. Translation Pipeline

The translation process shall follow these steps:

1.  **Locate:** Identify all files to be translated based on the input path and recursion settings.
2.  **Chunk:** Split the content of each file into smaller, manageable chunks suitable for the selected translation engine.
3.  **Translate:** Translate each chunk using the specified engine.
4.  **Merge:** Combine the translated chunks to reconstruct the full translated content of each file.
5.  **Save:** Write the translated content to the destination.

### 2.3. Content-Type Detection

-   The tool shall automatically detect if a file's content is HTML and handle it appropriately to preserve markup during translation.

## 3. Translation Engines

The tool shall support multiple translation engines.

### 3.1. Pre-integrated Engines

-   The tool shall integrate with the `translators` and `deep-translator` Python packages, allowing users to select any of their supported engines (e.g., `google`, `bing`, `deepl`).

### 3.2. Custom LLM-based Engines

#### 3.2.1. `hysf` Engine

-   **Provider:** Siliconflow
-   **Model:** `tencent/Hunyuan-MT-7B`
-   **Implementation:** Use the `openai` Python package to make API calls to the Siliconflow endpoint (`https://api.siliconflow.com/v1/chat/completions`).
-   **Authentication:** The API key shall be retrieved from the configuration.
-   **Resilience:** API calls shall be wrapped with `tenacity` for automatic retries.

#### 3.2.2. `ullm` (Universal Large Language Model) Engine

-   **Configurability:** This engine shall be highly configurable, allowing users to define profiles for different LLM providers. Each profile shall specify:
    -   API base URL
    -   Model name
    -   API key (or reference to it)
    -   Temperature
    -   Chunk size
    -   Maximum input token length
-   **voc Management:**
    -   The engine shall support a "prolog" in the first chunk, which can contain a JSON object of predefined voc.
    -   The prompt shall instruct the LLM to return the translation within an `<output>` tag.
    -   The prompt shall also instruct the LLM to optionally return a `<voc>` tag containing a JSON object of newly established term translations.
    -   The tool shall parse the `<voc>` output, merge it with the existing voc, and pass the updated voc to subsequent chunks.
-   **voc Persistence:**
    -   A `--save-voc` flag shall enable saving the final, merged voc as a JSON file next to the translated output file.

## 4. Configuration

-   **Storage:** Configuration shall be stored in a user-specific directory using the `platformdirs` package.
-   **Credentials:** The configuration shall securely store API keys. It must support storing either the raw API key value or the name of an environment variable that holds the key.
-   **Engine Settings:** The configuration shall allow specifying engine-specific settings, such as chunk sizes.

## 5. Command-Line Interface (CLI)

-   The tool shall provide a CLI based on `python-fire`.
-   The main command shall be `translate`.
-   **CLI Arguments:**
    -   `path`: The input file or directory.
    -   `--from-lang`: Source language (default: `auto`).
    -   `--to-lang`: Target language (default: `en`).
    -   `--engine`: The translation engine to use.
    -   `--recurse` / `--no-recurse`: Enable/disable recursive file discovery.
    -   `--write_over`: write_over original files instead of saving to an output directory.
    -   `--output`: The directory to save translated files.
    -   `--save-voc`: Save the voc file.

## 6. Python API

-   The package shall expose a Python API for programmatic use.

## 7. Dependencies

-   `translators`
-   `deep-translator`
-   `openai`
-   `tenacity`
-   `platformdirs`
-   `python-fire`
-   `semantic-text-splitter` (or similar for chunking)
