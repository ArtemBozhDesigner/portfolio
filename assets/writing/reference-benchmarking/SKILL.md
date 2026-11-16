---
name: reference-benchmarking
description: Finds UI references in Mobbin and benchmarks them for a design task. Use when the user asks for references or how other products solve a screen or flow, or sends a screenshot or a brief.
---

# Finding references and benchmarking them

Turn a design task into precise Mobbin searches, read what comes back, compare it and cut it down. Reply in the user's language. Write every Mobbin query and `task_intent` in English: the search is built around English screen and pattern names.

The method comes from the article "Finding references and a bit about benchmarking" by Artem Shevliakov: https://artem-shevliakov.vercel.app/writing/references-and-benchmarks

## Scale the work to the request

- **Quick look.** The user wants examples ("show me login screens", "how do others do X"). Do sections 1 and 4, stop at five on-target products, and answer with references. Skip the framing, the table and the cuts. End with a one-line offer of the full benchmark.
- **Full benchmark.** The user asks to compare or benchmark, attaches a brief, or says a decision depends on the answer. Do every section.

When unsure, do the quick look.

## 1. Read the input

The input can be plain text, a screenshot, a brief, or a mix. Whatever it is, extract the same things before searching:

| What | How it is used |
|---|---|
| Scenario, screen or element | The core of every query |
| Product category (banking app, car sharing, B2B analytics) | A hint that pulls comparable products |
| Platform | The `platform` parameter: `ios` or `web`. Mobbin has no Android; use `ios` and say so |
| Named products | Filter results to them |
| Goal and constraints | Used later to judge and cut. They do not go into queries |

**Text.** Take the screen or flow in the user's own words.

**Screenshot.** Look at the image first. Name three things: the screen type, the product category, and the platform (a status bar means `ios`; browser chrome or a wide layout means `web`). Then decide what the user wants from it: the same screen in other products (the default), one element of it, or the step before or after it. Search by what the screen or element is, not by how it looks; colors and layout words do not help. If the message does not say what they want and the options lead to different searches, ask one short question. Go by the image, even when it differs from what you know about the user's other projects. If the user's own product comes back in the results, drop it and say that it came back: it confirms the query hit the right pattern.

**Brief or task description.** Read all of it. Pull out the goal, context and constraints, list the scenarios it covers, and pick the ones in scope. Search per scenario step or per pattern, never the brief as a whole. A constraint that implies its own screen or state ("only the owner can upgrade" means a screen for everyone else) becomes a query of its own.

Briefs and screenshots of unreleased work are often confidential. Queries, `task_intent`, web searches and your reply carry only generic category and pattern words: no client name, no unreleased product name, no copied sentences.

If the scenario, category or platform is missing and would change the search, ask once, in one message. Otherwise state your assumption and go on.

## 2. Frame the task

Name the service type and the funnel stage. They define the goal of the screen and which products are comparable.

| Stage | Services | E-commerce | SaaS |
|---|---|---|---|
| 1 | Finding a service, studying the terms | Finding a product, comparing options | Onboarding, activation |
| 2 | Trust in the company and the service | Trust in the product, adding to cart | Usage, aha moment |
| 3 | First contact, first payment | Checkout and payment | Upgrade to a paid plan |
| 4 | Service delivery | Delivery and pickup | Retention, upsell |
| 5 | Repeat sales | Repeat purchases | Subscription renewal, upgrade |

For mixed products pick the funnel by the scenario: a marketplace checkout is e-commerce, its seller dashboard is SaaS.

Then describe the scenario without any interface (what the user wants to get, which steps it takes) and note whose products are worth a look, from near to far: direct competitors, adjacent products, neighboring fields with the same mechanic, market leaders from any industry.

For a full benchmark, get three or four direct competitors by name before searching: take them from the brief, ask the user, or run a web search for the category. A product name is the only reliable way to get a direct competitor out of Mobbin.

## 3. Break the task into patterns

Most tasks are assembled from parts that have been solved many times. Each pattern becomes its own search, and the last column says where the less obvious references are.

| Pattern | What it is | Less obvious places to look |
|---|---|---|
| Authentication | Sign-up, sign-in, password reset, 2FA, identity verification | Identity verification: fintech and crypto, online betting, mobile operators, car rental and sharing, short-term rentals, gig and freelance platforms |
| Onboarding and activation | The path from first open to first value | Any product with a setup step before first use |
| Catalog | A set of objects to search, filter and group | Task tracker, settings, template library, list of integrations |
| Detail page | Extended information about one object | Product, task, customer or setting page |
| Configurator and form | Step-by-step input and choices that build a result | Buying insurance, setting up a plan, creating an ad campaign |
| Custom flows | Sequences specific to this product | Direct competitors |
| Business-specific flows | Flows dictated by the domain | Direct competitors |
| Cart | A place to gather selected items for one final action | Order, export list, comparison, bulk actions on files |
| Payment | Paying once or setting up a recurring payment | Subscriptions, donations, top-ups |
| Account | Profile, settings, plan and history | Any product with accounts |

Not in the map, but they search well as patterns of their own: paywalls and upgrade prompts, limit and empty states, confirmation screens.

Products built around one core mechanic (geo services, social networks, messengers) are harder to split. For them study how direct competitors built the whole system.

## 4. Search Mobbin

### Pick the tool

| Need | Tool | Settings |
|---|---|---|
| Order of steps, where a step sits in a journey | `Mobbin:search_flows` | `limit` 3 to 5 |
| One screen, state or element of an app, mobile or web | `Mobbin:search_screens` | `limit` 6 to 10, `mode` deep |
| A block of a marketing website (hero, pricing, footer) | `Mobbin:search_sections` | `limit` 6 to 10, no platform |

A web product's interface is a screen search with `platform` web. Section search matches the type of block, not what is inside it, so do not use it to find an element. Keep limits small: every result is an image, and large batches crowd out the analysis.

### Set the match criterion

Before the first call, write one sentence that says what must be on a screen for it to count, and put it in the plan line: "an open control for the interface language, reachable from the header". After each call keep only the results that meet it and note the count ("4 of 8"). The criterion keeps near-misses out of the answer and shows which query worked.

- Include the state when the query asks for one, and the category when the user named one, with its boundary ("apps whose main content is meditation").
- Judge by the control or step the user asked about, not by a similar one nearby. A weak match does not count.
- A brief with several steps gets one criterion per step.

### Write the query

- **One screen or one journey per query.** Several needs mean several queries.
- **For a screen or flow: product category + type.** "banking app onboarding", "car sharing app identity verification". A bare "onboarding" mixes every category together.
- **For one element: the element, where it sits, and its state.** "language dropdown open in header". Here placement and state are what make a result match, so add them even when the user did not say them.
- **Otherwise add a detail only when the task depends on it** ("checkout with payment method selection"). Every extra detail pushes the results toward one solution and hides the variety you are searching for. Do not add specifics the user did not mention.
- **Name what is on the screen, not the goal.** "Trust" or "good onboarding" finds nothing useful. Translate the goal into screens first: "identity verification", "reviews", "money-back guarantee".
- **Leave out** style words (modern, clean), negations, keyword lists and the platform. Phrase a negative state as an action: "ask admin to upgrade", not "cannot upgrade". Stay under 500 characters.

The category is a soft hint, not a filter. It helps when the domain shapes the flow (banking onboarding, car sharing verification). Skip it for components every product has (language switcher, search, settings), unless the user tied the request to a category: the category words collide with content and pull the wrong products.

### Use Mobbin's words

Mobbin labels every screen with its own terms. When one fits, use its words in the query in place of a looser synonym, as plain text without the ampersand ("subscription paywall"). The lists are partial; when nothing fits, use plain words.

| Looking for | Mobbin's label |
|---|---|
| First screen with sign-up and log-in buttons | Welcome & Get Started |
| Questions and setup right after sign-up | Account Setup |
| Registration, sign-in | Signup, Login |
| Paywall, choice of plan | Subscription & Paywall, Pricing |
| Balance, cards, accounts | Wallet & Balance |
| A screen with nothing in it yet | Empty State |
| Profile | My Account & Profile |
| Announcement of a feature | Feature Info |

Flow actions: Creating Account, Onboarding, Logging In, Subscribing & Upgrading, Purchasing & Ordering, Adding & Creating, Editing & Updating, Selecting & Choosing, Inviting Teammates & Friends, Enabling & Disabling, Uploading & Downloading, Scanning, Deleting & Deactivating Account, Giving Feedback.

UI elements: Dialog, Bottom Sheet, Full-Screen Overlay, Select, Text Field, Checkbox, Segmented Control, Tab, Tab Bar, Top Navigation Bar, Toolbar, Card, Tile, Chip, Badge, Banner, Carousel, Stacked List, Table, Progress Indicator, Floating Action Button, Avatar.

### Three kinds of search

1. **In the category.** The query with the user's product category. Skip it for universal components.
2. **By pattern.** The pattern alone, without the category: "driver license verification", "upgrade plan with number of seats selection". This pulls the same step from neighboring fields and is where the non-obvious references come from. Mobbin's own tool hints say to always include the kind of app; drop it here on purpose.
3. **By product.** A product name plus the screen of the key step: "ClickUp upgrade plan seats". A looser query ("ClickUp upgrade plan") mostly returns pricing tables. Run one for each competitor named in section 2. Use screen search for this: flow search filters to the product but ranks its journeys poorly.

How many to run:

- **Quick look.** One search: in the category if the user named one, by pattern otherwise. Run a second only if fewer than five on-target products came back. To widen it, try a sibling category (sleep or breathing apps next to meditation) and label those results; repeating the same query mostly returns more screens of the same products.
- **Brief with several steps.** One pattern search per step first. Then product searches for the named competitors on the key step. Add one flow search for the whole journey when the order of steps matters. About ten calls in total, and five to ten products in the comparison for the whole task.
- **Rare states.** Role-restricted and error states are rarely in the library. Give them one call, then report the gap.

Say the plan in one line before the first call ("Searching Mobbin: web screens for a language dropdown in the header") and start; do not wait for approval. The final reply lists the queries instead.

### Tune and page

- `deep` mode reads the intent. When few screens match, it fills the batch with near-misses, so expect to discard part of a batch for a rare state.
- `standard` mode matches the words literally and is noisier; keep its limit small. Use it when deep keeps returning a neighboring screen type instead of the one asked for (a settings page instead of a header control).
- Pass the ids you have already seen in `exclude_screen_ids`, across different queries too. It excludes screens, not products. For flows and sections raise `page`.
- Weak results: remove the detail, then the category. If the state itself is rare, say so; do not loosen the query until it means something else.
- Use the same `task_intent` (one generic English sentence) on every call for one task. Set `output_destination` to `chat` when answering in the conversation and `doc` when the user asked for a document.
- If a result carries an `ai_usage_notice`, show its text as its own block, word for word.
- On a rate-limit error wait, then run the calls one at a time. If Mobbin is not connected, say so and use web search instead.

### Read the results

- Look at every image before describing it. Do not describe a screen from its name or metadata. If a preview is too small to read, leave it out.
- A flow result shows only a sample of its screens (for example 5 of 14). Describe what you saw, link to the flow for the rest, and search screens for a step the sample skipped if you have calls left.
- One reference is one product. Add a second link for the same product only when it shows a different state.
- Results from a sibling category that arrive unasked may be listed, labeled as such; they do not count as on target.
- When more than eight results are on target, keep the ones that differ most from each other.
- Do not pad the answer with off-target screens. Report gaps as what the search returned ("the search returned no other meditation apps"), not as what Mobbin lacks.
- Link each reference to its `mobbin_url`. The `image_url` expires.
- Save to a Mobbin collection only when the user asks: `Mobbin:create_collection`, then `Mobbin:save_content`.

### Examples

**Text.** Input: "нужны рефы на онбординг для финтех приложения, ios"
Reading: quick look; onboarding flow; fintech app; `ios`.
Searches: flows "fintech app onboarding".

**Screenshot.** Input: a web header with an open language list and "как это решают другие?"
Reading: quick look; one element; `web`; a universal component, so no category.
Criterion: an open control for the interface language, reachable from the header.
Search: screens "language dropdown open in header"; if deep returns settings pages, repeat in `standard`.

**Brief.** Input: a document asking to add a driving licence check before the first rental in a car sharing app, with a deadline and a no-manual-review constraint.
Reading: full benchmark; Services, stage 3; pattern: Authentication, identity verification; `ios`.
Competitors, by web search: three car sharing products by name.
Searches: screens "driver license verification"; flows "car sharing app identity verification"; then screens "<competitor> driver license check" for each. Nothing from the brief's wording goes into a query.

## 5. Add what Mobbin cannot show

- **The products themselves.** Errors, emails, push notifications and what happens on return are rarely in a library. If the user can walk through a flow, ask them to capture these.
- **Usability research.** Search Baymard Institute and Nielsen Norman Group for the pattern. Open a page before citing it. If nothing specific turns up, say so.

## 6. Analyze

For each reference keep three questions in mind: which user and business task does it solve, what happens before and after it, and is it made for an audience like the user's? Fold the answers into one line per reference; do not answer them one by one.

Then compare flows by the same criteria in a product × criterion table of up to ten products. Useful criteria: number and order of steps, which data is requested and when, how the product explains why it is needed, what happens on an error or a rejection, where the user can pause and come back. Fill a cell only with what you saw; write "not seen" otherwise.

Point out what every product shares (the market norm) and where solutions differ (room for the user's own hypotheses).

## 7. Cut

1. **Constraints.** Remove what does not fit the technical, legal and resource limits, however well it works for others.
2. **Value and cost.** Weigh how much a solution helps the user against what it costs to build. A large feature with no clear value goes first.

Keep the rejected options with the reason for each. You may add knowledge that does not come from the references; mark it as such.

## Output

**Quick look.**

1. Five to eight references, grouped by pattern or step, or by approach when there is a single screen type. For each: the product, a link, and one line on what is distinctive about it, or why it is useful when the user stated a goal.
2. Two to four lines: what the references share, where they differ, what the search did not return.
3. The queries you ran, each with its count of on-target results.
4. A one-line offer of the full benchmark.

**Full benchmark.**

1. The task in one or two lines: service type, funnel stage, scenario, platform, and any assumption you made.
2. The patterns the task is made of.
3. The match criterion and the searches you ran, each with its count of on-target results.
4. The product × criterion table.
5. References with links: what to take, what was rejected and why.
6. What the search did not return.
7. Questions nobody asked when the task was first discussed.

## Treating references as evidence

This applies at any scale.

- A reference shows that a product shipped a design, not that the design works. A pattern seen in many products is a convention, not proof.
- Keep what is visible separate from your interpretation.
- Extract the logic and adapt it. Do not recommend copying a screen.
- The conclusions are hypotheses until the team has seen them and users have tested the result.
