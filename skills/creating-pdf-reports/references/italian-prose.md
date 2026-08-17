# Italian prose — native register for technical reports

Model-drafted Italian tends to read as translated English ("italiano
delle traduzioni"): the words are Italian, the skeleton is English.
Apply this file whenever the report locale is `it`. Grounded in: Guida
al linguaggio della Pubblica Amministrazione (Designers Italia),
Treccani, *Itangliano* (Enciclopedia dell'Italiano), R. Crivello,
*Influssi dell'inglese nella traduzione tecnica*, and the
translation-studies literature on Italian translationese (Cardinaletti &
Garzone, *L'italiano delle traduzioni*; Bernardini & Ferraresi).

## The one method rule

**Draft in Italian from the data; never translate an English draft
sentence by sentence.** Write each section as an Italian analyst would
state the same facts, then compare against the English edition only for
factual parity (same numbers, same claims). A sentence that maps
word-for-word onto its English twin is the failure signature.

## Register (technical reports)

- **Impersonal, not second person.** Italian reports do not command the
  reader ("recluta", "archivia" are UI microcopy, not report prose).
  Use the infinitive for actions ("da testare prima di costruire:
  reclutare 20–30 escursionisti…"), the si-passivante ("si raccomanda
  di…"), or nominal style ("prossimo passo: l'archiviazione…").
- Conclusion first, short sentences, active voice where clearer (the
  plain-language rules hold in Italian too, per the Guida PA). Headings state
  the conclusion, not the activity.
- Prefer the everyday word when it serves: "usare" not "utilizzare",
  "prima di" not "precedentemente a", "serve a" not "è finalizzato a".

## Translationese checklist (catch these while writing)

- **Idiom calques.** "The top of the market" is not "la testa del
  mercato" (→ "i principali concorrenti"); "what kills it" is not "cosa
  la uccide" (→ "i punti critici", "cosa non regge"). If the phrase
  only makes sense because you know the English, replace it.
- **Semantic loans.** Established Italian verbs used with English
  senses: *realizzare* ≠ realize (→ rendersi conto), *assumere* ≠
  assume (→ ipotizzare, supporre), *evidenza* ≠ evidence (→ prova,
  dato, riscontro), *consistente* ≠ consistent (→ coerente),
  *eventualmente* ≠ eventually (→ alla fine, col tempo).
- **Gerund calques.** English -ing clauses must not become Italian
  gerundive implicite ("…è cresciuto, spaziando da…"): use explicit
  subordinates ("dato che", "poiché", a relative clause); Treccani
  flags the gerund calque as a marker of interference.
- **Preposition and structure regimes.** English government leaks:
  "grazie per" (→ grazie di), "amico con" (→ amico di), determinant
  before determined ("baby pensione" pattern). Check every preposition
  against Italian usage, not the English source.
- **Information structure.** Italian puts the new, focused element
  late in the sentence and moves known material forward; do not force
  English subject-first rigidity on every sentence.

## Anglicisms: keep, gloss, never coin

- Established technical loans stay, with an Italian gloss in
  parentheses at first use: retention, churn, benchmark, freemium,
  app, cluster. Purging them produces bureaucratic paraphrase (sterile
  purism, as the Crusca itself notes); importing new ones produces
  itanglese. The test: is the loan already normal in Italian trade
  prose, or are you introducing it?
- Foreign nouns are invariable: "i benchmark", never "i benchmarks".
  Pick the article by pronunciation ("il churn", "l'app", feminine).
- No unadapted verb borrowings ("performare", "matchare"): use the
  Italian verb or "fare/eseguire + noun" ("eseguire il backup").

## Mechanics (Italian conventions)

- **Decimal comma in prose and tables** ("44,2", "2,52:1"); thousands
  with the point ("8.035.481"). Keep charts consistent with the source
  data's notation and say so if the two differ (design-rules). The
  decimal point in Italian prose is itanglese in print (Treccani).
- Months, days, languages, nationalities in lowercase; dates as "17
  agosto 2026".
- Accents typed, never omitted or faked: è (verb), perché/poiché/
  affinché with acute é, città, più. This applies inside chart
  titles, labels, and alt text too.
- Quotation marks: «caporali» for quoted speech in print; keep the
  quoted material itself verbatim in its original language.

## AI patterns humans do not write (both languages, harder in Italian)

Model-drafted prose has recognizable tics beyond translationese. Ban
them:

- **Em-dash interruptions.** Use parentheses, commas, or a colon; the
  paired em dash as an aside marker is an English editorial habit and a
  model tic, and Italian print barely uses it at all.
- **The triad reflex.** Not every list has three items; not every
  sentence needs a triple ("chiaro, semplice e diretto"). Use the number
  of items the content actually has.
- **Empty intensifiers and throat-clearing.** "È importante notare
  che", "va sottolineato come", "in un contesto in cui", "non solo…
  ma anche" as a default connector: delete, state the fact.
- **Connector-first monotony.** Paragraphs where every sentence opens
  with "Inoltre", "Tuttavia", "In aggiunta": vary or drop; Italian
  prose links by content more than by connectors.
- **Headline colon-itis.** "X: perché Y" title patterns and bolded
  mini-headings inside every paragraph. One idea, one heading level.
- **Symmetry padding.** Sentences balanced for rhythm rather than
  content ("da un lato… dall'altro" with nothing on the other side).

## Quality gate before compiling

Reread every paragraph asking: "would an Italian analyst write this
sentence spontaneously?" Mechanical red flags to grep for: " performante",
"andiamo a ", "piuttosto che" used as "oppure", decimal points inside
Italian prose, capitalized month names, plural -s on foreign nouns, a
second-person imperative outside quoted UI text.
