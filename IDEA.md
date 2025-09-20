
We want a `abersetz` Python package that performs language translation of text in files. Single file or multiple files. We also want a Fire CLI tool. 

Copy structure and ideas and overall functionality from @external/cerebrate-file.txt

The working scheme is: 

- We locate files
- We split the files into chunks
- We translate the chunks
- We merge the chunks 
- We save the translated files into a new folder or we write_over

https://pypi.org/project/translators/ ships with a CLI tool called 'fanyi' that can be used to translate text: 

```
>fanyi --help                                                                                                                          usage: fanyi input [--help] [--translator] [--from] [--to] [--is_html] [--version]

Translators(fanyi for CLI) is a library that aims to bring free, multiple, enjoyable translations to individuals and students in Python.

positional arguments:
  input                 raw text or path to a file to be translated.

options:
  --help                show help information.
  --translator          e.g. bing, google, yandex, etc...
  --from                from_language, default `auto` detected.
  --to                  to_language, default `en`.
  --is_html             is_html, default `0`.
  --version             Show version information.
```

Our tool should use the 'recurse' flag like @external/cerebrate-file.txt . It should not translate text but should translate files instead (similar to @external/cerebrate-file.txt ).


We do need this mechanism: 

```
  --from                from_language, default `auto` detected.
  --to                  to_language, default `en`.
```

As for HTML, we should actually have some sort of DETECTION of HTML. 

We need to connect our package to "translators" and "deep-translator" packages, and use the translator engines from there easily. 

But on top of that, we also implement our own translator engines. 

The first custom engine is 'hysf' (hunyuan/siliconflow). It should work by calling the OpenAI package with the siliconflow API and the model name 'tencent/Hunyuan-MT-7B'. The model has a 33k token window and the prompt format is like so (using curl):

And then, we also need to use the platformdirs package to store the API keys (in a dual form: we either store the env var name or the actual value), and other configuration. For example chunk sizes for various translator engines. 



```
curl -s --request POST --url https://api.siliconflow.com/v1/chat/completions --header "Authorization: Bearer ${SILICONFLOW_API_KEY}" --header 'Content-Type: application/json' --data '{"model":"tencent/Hunyuan-MT-7B","temperature":1.0,"messages":[{"role":"user","content": "Translate the following segment into Polish, without additional explanation.\n\nMYTEXT"}]}' | jq -r '.choices[0].message.content'
```

where MYTEXT is the text to translate, and Polish is the target language. We should use the OpenAI Python package plus tenacity to handle the API calls.

The second custom engine is 'ullm' (universal large language model) with configurable API endpoint provider URLs, model names, API key env var names or values, temperature, chunk size, and max input token length. See @external/dump_models.py for examples of LLM configurations. 

The implementation of the LLM engine should be similar to @external/cerebrate-file.txt but using the OpenAI Python package plus tenacity to handle the API calls. 

The main point is that the first chunk for the translation input should be sent with a potentially configured "prolog" which would typically be a custom voc expressed in JSON. 

The LLM prompt request for the translation to be output inside the `<output>` tag, and optionally would (in the same call) include `<voc>` where the prompt would request the model to output a same-formatted JSON that would include "newly established custom voc". The idea is that the model should be able to translate, and then also output the most important translations as a from-to dict so that subsequent chunks could translate the same stuff consistently. 

Our tool would parse for those voc outputs and would merge that into our running voc (and add it into the next chunk). We could also give the tool the --save_voc param and then in addition to the saved chunk, our tool would save the updated voc JSON next to the output file. 

<TASK>

1. Now /plan all this into @PLAN.md 

2. Into @TODO.md write a flat linear list of `- [ ]` itemized tasks. 

3. Replace @README.md with a detailed explanation of what our package does, how it works and why. 

4. Edit @CLAUDE.md : keep its contents but at its very beginning add all the contents of the new @README.md 

5. Start implementing tasks from @PLAN.md and @TODO.md  

6. Create an `examples` folder and write actual real examples there. 

7. Review, analyze, verify, test (on actual real examples). 

8. Refine, improve, iterate. 

Focus all your efforts on producing a lean, performant, focused minimal viable product. Eliminate unnecessary fluff. Minimize custom code if ready-made code can be used. 
</TASK>

## Potential dependencies

- https://github.com/benbrandt/text-splitter (see @external/text-splitter.txt and @external/semantic-text-splitter.txt )
- https://pypi.org/project/tokenizers/ (see @external/tokenizers.txt ) 
- https://pypi.org/project/tiktoken/ (see @external/tiktoken.txt )
- https://pypi.org/project/ftfy/ (see @external/python-ftfy.txt )
- https://pypi.org/project/langcodes/ (see @external/langcodes.txt )
- https://github.com/openai/openai-python
- tenacity
- deep-translator (see @external/deep-translator.txt )
- https://pypi.org/project/translators/ ( see @external/translators.txt )
- https://github.com/tox-dev/platformdirs ( see @external/platformdirs.txt )