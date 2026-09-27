# HW1 submission

**Name:**
**Student ID:**
**Group:**
**Repository:**

## AI tool disclosure

State which AI tools you used and for what. Expected and fine; undisclosed use
is not.

>I used ChatGPT (GPT-5.6 Sol) to discuss the assignment requirements, help with Python implementation and debugging, and interpret the results of my experiments.
>
>Specifically, ChatGPT helped me draft and refine:
>- the course-registration system prompt in Sublab Easy;
>- the Kazakh correction prompt in Sublab Medium, including the instruction to preserve the original punctuation;
>- the implementation and analysis for the tokenizer experiments in Sublab Harder.
>
>For the experiments themselves, I used the models required by the assignment through the OpenAI and OpenRouter APIs. The token counts, costs, model outputs, correction results, and tokenizer measurements reported in `SUBMISSION.md` come from my own program runs.

---

## Sublab Easy — the registration bot and its bill

**How I laid the catalogue out inside the system prompt, and why:**

> I included the complete catalogue, registration rules, and student data as formatted JSON inside the system prompt. I
> chose JSON because it preserves the original structure of the data and makes course codes, credits, prerequisites,
> meeting times, seat availability, and student information easy for the model to distinguish. I also added explicit
> instructions not to invent courses or information that was not present in the catalogue.

**My turn 5 (Kazakh or Russian):**

> Я студент третьего курса. Куда я все еще могу зарегистрироваться

### Run 1 — OpenAI, `gpt-5.6-luna`

| Turn      | Input tokens | Output tokens | Cost $   |
|-----------|--------------|---------------|----------|
| 1         | 1358         | 312           | 0.000646 |
| 2         | 1584         | 261           | 0.000630 |
| 3         | 1739         | 75            | 0.000438 |
| 4         | 1833         | 49            | 0.000425 |
| 5         | 1904         | 311           | 0.000754 |
| **total** | 8,418        | 1,008         | 0.002893 |

### Run 2 — OpenRouter, `google/gemma-4-26b-a4b-it:free`

| Turn      | Input tokens | Output tokens | Cost $   |
|-----------|--------------|---------------|----------|
| 1         | 1626         | 523           | 0.000183 |
| 2         | 2175         | 95            | 0.000112 |
| 3         | 2295         | 135           | 0.000126 |
| 4         | 2453         | 30            | 0.000110 |
| 5         | 2506         | 524           | 0.000221 |
| **total** | 11,055       | 1,307         | 0.000752 |

### Turn 4, verbatim

The turn where you asked for CSS-4090, which does not exist. Paste both replies
exactly as they came back — do not tidy them.

**OpenAI:**

```
I cannot add **CSS-4090 — Quantum Machine Learning** because it is **not in the provided course catalogue**. Therefore, its credits, prerequisites, seat availability, and schedule cannot be verified, and registration is refused.
```

**OpenRouter:**

```
I cannot add **CSS-4090 Quantum Machine Learning** to your schedule because this course code is not present in the provided catalogue.
```

### Written answers

**1. The two providers used almost identical code. What actually changed, and
what did not?**

> The main differences were the API key, the base_url, and the model name. For OpenAI I used the default OpenAI
> endpoint, while for OpenRouter I used the same OpenAI client with https://openrouter.ai/api/v1 as the base_url.
>
> The rest of the code stayed almost the same. Both providers used the same OpenAI Python library, the same
> chat.completions.create() method, the same message format with system, user, and assistant roles, and the same way of
> reading the response and token usage. This showed that OpenRouter is compatible with the OpenAI API format.

**2. Why did the input token count climb on every turn when your questions
stayed roughly the same length? Use the numbers from your own table. What
happens to the bill at fifty turns?**

> The input token count increased because every request sends the whole conversation history again. The model does not
> remember previous turns by itself.
>
>For GPT-5.6 Luna, the input tokens increased from 1,358 on turn 1 to 1,584, 1,739, 1,833, and finally 1,904 on turn 5.
>
>For Gemma, the increase was even larger: 1,626 → 2,175 → 2,295 → 2,453 → 2,506 input tokens.
>
>The questions themselves were still short, but previous user messages and model answers became part of the next input.
> For example, Gemma produced a long 523-token response on turn 1, and much of that content had to be sent again on turn

2.

>
>If the conversation continued for fifty turns, later requests would contain a much larger transcript. This means that
> each new turn would generally become more expensive, and the total bill would grow faster because old messages would
> be
> paid for repeatedly.

**3. Turn 4: did the bot refuse, or did it invent CSS-4090?** If it refused, what
in your system prompt held the line? If it invented, what did it make up —
credits, a room, an instructor?

> Both models refused the request and did not invent CSS-4090.
>
>GPT-5.6 Luna said that CSS-4090 was not in the provided course catalogue and refused to register it because the
> credits, prerequisites, seats, and schedule could not be verified. Gemma also directly stated that the course code was
> not present in the catalogue.
>
>I think the strongest part of the system prompt was the explicit instruction to use only the provided catalogue and to
> never invent a course, course code, credits, prerequisites, schedule, instructor, room, or seat availability. It also
> specifically instructed the model to refuse a requested course if its code was not present in the catalogue.

**4. Where else was either bot wrong?** Turn 2 asks for two courses that meet at
the same hour; two courses in the catalogue are full. Did the bots notice?

> Both models noticed the timetable conflict in turn 2. They correctly identified that CSS-4007 and CSS-4102 both meet
> on Tuesday from 09:00 to 10:50, so they refused to register both at the same time.
>
>They also noticed the full-course restriction. Both identified CSS-4400 as unavailable because it had no remaining
> seats. Gemma additionally mentioned that CSS-3011 was full, although the student had already completed it anyway.
>
>There were still some reasoning problems. GPT-5.6 Luna focused on the maximum credit limit and said that the 11 credits
> from CSS-4007 and CSS-4102 were within the 30-credit maximum, but it did not mention the minimum-credit requirement.
> Gemma did notice the 15-credit minimum in turn 3.
>
>Gemma also produced an inconsistent answer in turn 1: it initially placed several already completed courses under
> “Eligible Courses” and then corrected itself inside the same answer. Its final conclusion was mostly correct, but the
> structure of the answer was confusing.

---

## Sublab Medium — one task, six models

Paste the per-model summary printed by `correct_kazakh.py`:

| Model                           | Exact | Failed | Tokens | Cost $  |
|---------------------------------|-------|--------|--------|---------|
| google/gemma-4-26b-a4b-it:free  | 4     | 0      | 11269  | 0.00209 |
| qwen/qwen3.8-27b                | 5     | 0      | 50471  | 0.15431 |
| deepseek/deepseek-v4-flash-0731 | 7     | 0      | 27706  | 0.00738 |
| gpt-5.6-luna                    | 8     | 0      | 3924   | 0.00271 |
| gpt-5.6-terra                   | 8     | 0      | 3034   | 0.01645 |
| gpt-5.6-sol                     | 8     | 0      | 3170   | 0.04520 |

### Which error types did each model repair?

Rows are error labels, columns are models. Write "yes", "no" or "partial".

| Error type      | gemma   | qwen    | deepseek | luna | terra | sol |
|-----------------|---------|---------|----------|------|-------|-----|
| kaz_to_rus      | partial | partial | yes      | yes  | yes   | yes |
| latin_homoglyph | partial | yes     | yes      | yes  | yes   | yes |
| drop_hyphen     | no      | yes     | yes      | yes  | yes   | yes |
| join_words      | yes     | yes     | yes      | yes  | yes   | yes |
| double_letter   | yes     | yes     | yes      | yes  | yes   | yes |

**The `latin_homoglyph` row: what happened?** Describe what you observed. The
explanation is Sublab Harder's job, not this one's.

> Most models were able to recognize and replace the Latin lookalike characters with the correct Cyrillic characters.
> DeepSeek, Luna, Terra, and Sol handled the latin_homoglyph examples correctly. Qwen also identified and repaired the
> homoglyphs themselves, although in KZ-08 it introduced an unrelated spelling error elsewhere in the sentence. Gemma
> was
> less consistent: it handled KZ-08 correctly, but in KZ-03 it changed Aлaяқtарға to Алақтарға, losing part of the word.
> Therefore, the main observation is that visually similar Latin characters were not equally easy for all models to
> repair, and performance could vary even between two examples of the same error type.

**Where a model returned good Kazakh that was not identical to the original,
say so here.** Exact match is not correctness.

> The clearest case was DeepSeek on KZ-01. It repaired all of the corrupted Kazakh letters correctly, but added a period
> at the end of the sentence. Because the published original had no final period, the automatic comparison marked it as
> exact = false with char_diff = 1. The sentence itself was still correct Kazakh, so I would count this as a successful
> correction even though it was not an exact string match.
>
>Other non-exact cases in the final run were mostly real errors rather than harmless differences. For example, Gemma
> failed to restore the hyphen in KZ-02 and damaged the first word in KZ-03, while Qwen introduced unrelated spelling
> errors in some sentences.

**Cheapest model that was good enough, and why:**

> The cheapest model that I would consider good enough was GPT-5.6 Luna. Gemma was slightly cheaper overall, costing
>
about $0.002091 for the eight sentences, but it produced only 4/8 exact matches and made several real correction errors. Luna cost about $
> 0.002713 in total and produced 8/8 exact matches, correctly handling every error type in the dataset, including
> latin_homoglyph, drop_hyphen, join_words, double_letter, and kaz_to_rus.
>
> The difference in total cost between Gemma and Luna was only about $0.00062 for the whole experiment. For that very
> small additional cost, Luna was much more consistent, so it was the cheapest model in my run that I would consider
> reliably good enough for this task.

---

## Sublab Harder — open the tokenizer

### A. What a language costs

**`cl100k_base`:**

| Language | Tokens | Chars | Tok/char | × English | $ per 1,000 sentences |
|----------|-------:|------:|---------:|----------:|----------------------:|
| kk       |    200 |   263 |    0.760 |      3.75 |                0.1667 |
| ru       |    129 |   277 |    0.466 |      2.30 |                0.1075 |
| en       |     59 |   291 |    0.203 |      1.00 |                0.0492 |

**`o200k_base`:**

| Language | Tokens | Chars | Tok/char | × English | $ per 1,000 sentences |
|----------|-------:|------:|---------:|----------:|----------------------:|
| kk       |     84 |   263 |    0.319 |      1.58 |                0.0700 |
| ru       |     74 |   277 |    0.267 |      1.32 |                0.0617 |
| en       |     59 |   291 |    0.203 |      1.00 |                0.0492 |

### B. What a homoglyph does

One row per `latin_homoglyph` sentence in the dataset. Paste the actual decoded
token strings around the divergence point, not a description of them.

| Sentence id | Foreign char (index, name)                                                                    | Tokens correct | Tokens corrupted | Δ  | Diverges at |
|-------------|-----------------------------------------------------------------------------------------------|----------------|------------------|----|-------------|
| KZ-03       | 0: `A` - LATIN CAPITAL LETTER A; 2: `a` - LATIN SMALL LETTER A; 5: `t` - LATIN SMALL LETTER T | 16             | 20               | +4 | 0           |
| KZ-08       | 1: `o` - LATIN SMALL LETTER O; 3: `a` - LATIN SMALL LETTER A; 9: `T` - LATIN CAPITAL LETTER T | 21             | 24               | +3 | 1           |

**Token pieces around the divergence:**

**KZ-03**

```
correct  : ['А', 'лая', 'қ', 'тарға', ' ақша']
corrupted: ['A', 'л', 'a', 'я', 'қ']
```

**KZ-08**

```
correct  : ['Д', 'он', 'аль', 'д', ' Т', 'рамп']
corrupted: ['Д', 'o', 'н', 'a', 'л', 'ль']
```

### C. Did it get better?

| Language | cl100k_base | o200k_base | Change          |
|----------|-------------|------------|-----------------|
| kk       | 0.760       | 0.319      | -0.441 (-58.0%) |
| ru       | 0.466       | 0.267      | -0.199 (-42.7%) |
| en       | 0.203       | 0.203      | 0.000 (0.0%)    |

### Written answers

**1. What is the Kazakh tax?** The ratio against English in both encodings, the
dollar figure from A, and how much it changed between the two tokenizers.

> With cl100k_base, Kazakh required 0.760 tokens per character, compared with 0.203 for English. This means Kazakh cost about 3.75× as many tokens per character as English. At the given input rate of `$`5 per million tokens, 1,000 average Kazakh sentences from this dataset would cost about `$`0.1667, compared with $0.0492 for English.
With o200k_base, Kazakh dropped to 0.319 tokens per character, while English stayed at 0.203. The Kazakh-to-English ratio therefore fell to about 1.58×, and the cost of 1,000 average Kazakh sentences fell to about `$`0.0700.
So the newer tokenizer reduced the Kazakh tokens-per-character value from 0.760 to 0.319, which is about a 58% reduction. The relative “Kazakh tax” also narrowed substantially, from 3.75× English to 1.58× English. It did not disappear, but it became much smaller.

**2. Why did the models repair `kaz_to_rus` but struggle with
`latin_homoglyph`?** Both are single-letter substitutions and both look almost
identical on screen. Use your token streams from B as the evidence. Say what the
model actually received in each case.

>The important difference is that kaz_to_rus substitutions still use Cyrillic characters, while latin_homoglyph introduces characters from a different Unicode script even though they look almost identical on screen.
Measurement B shows that the Latin homoglyphs changed the token stream substantially. In KZ-03, the correct version used 16 tokens, while the corrupted version used 20 tokens, an increase of 4. The streams diverged immediately at token index 0. The correct text was tokenized around the first word as:
['А', 'лая', 'қ', 'тарға', ' ақша']
while the corrupted version became:
['A', 'л', 'a', 'я', 'қ']
The tokenizer was therefore no longer seeing the same useful Kazakh pieces such as лая and тарға; the Latin A, a, and t caused the word to fragment differently.
KZ-08 showed the same effect. The correct version used 21 tokens, while the corrupted version used 24, and the streams diverged at index 1. The correct pieces included:
['Д', 'он', 'аль', 'д', ' Т', 'рамп']
while the corrupted version began:
['Д', 'o', 'н', 'a', 'л', 'ль']
So although kaz_to_rus and latin_homoglyph may look similar to a person, they are not equivalent to the tokenizer. In latin_homoglyph, the model receives different Unicode characters and a more fragmented token sequence. This gives the model a less familiar representation to repair. Our measurement directly demonstrates this for the Latin-homoglyph cases; the kaz_to_rus characters remain within the Cyrillic script rather than introducing these foreign Latin code points.

**3. Name one thing this measurement does not explain about your Sublab Medium
results.** You measured OpenAI's tokenizers; three of your six models were not
OpenAI's. What follows, and what would you have to do to close the gap?

> This measurement cannot directly explain the behavior of Gemma, Qwen, or DeepSeek, because cl100k_base and o200k_base are OpenAI tokenizers. Those three models may use completely different vocabularies and tokenization algorithms.
Therefore, the token fragmentation observed here is evidence for how this problem can affect OpenAI-style tokenization, but it is not proof that Gemma, Qwen, or DeepSeek received the same token sequence. To close this gap, I would need to obtain the actual tokenizer used by each non-OpenAI model and repeat the same experiment: encode the correct and corrupted sentences, compare token counts, find the first divergence, and inspect the decoded token pieces.
