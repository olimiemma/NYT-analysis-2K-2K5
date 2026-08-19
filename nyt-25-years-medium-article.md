## What 2.2 Million Headlines Taught Me About 25 Years of America

*I fed a quarter century of New York Times headlines into Python. What came back was a portrait of a nation's mood, one year at a time.*

---

There's a moment in every data project when a spreadsheet stops being a spreadsheet and starts being a story. Mine came about an hour into cleaning a dataset, when I noticed that a single row of "short description" text was 504,071 characters long. Somewhere in there, buried in a single cell meant to hold a sentence, was what looked like an entire article. Maybe a whole day's worth of them.

That's the thing about big datasets: they don't just contain information, they contain accidents, artifacts, and fingerprints left by the humans and systems that built them. Before I could ask any interesting questions, I had to become something between a detective and a janitor.

The dataset itself was simple on paper: every headline and short description published by the New York Times from January 1, 2000 to December 2025, scraped from their public API. Four columns. Over 2.2 million rows. Twenty-five years of a newsroom deciding, every single day, what mattered enough to put in front of millions of readers.

What follows is the story of what happened when I asked that dataset some real questions, the mistakes I made along the way, and what a quarter century of headlines actually reveals about how the tone of American public life has shifted.

### Before the Fun Part, the Cleanup

Every real dataset lies to you a little before it tells you the truth. Mine had three problems hiding under the surface.

First, duplicates: 1,413 articles had been counted twice, probably because the scraper pulled overlapping windows of time. Small, but worth catching.

Second, a handful of titles that were absurdly long, one clocking in near 6,000 characters, which is not a headline, that's a corrupted row where something went wrong in the original scrape.

And third, that 504,071-character description I mentioned. When I checked how many rows had descriptions over 1,000 characters, the answer was over 30,000. Something systemic was happening, likely full article bodies leaking into a field meant for a one-line teaser.

The fix was straightforward: drop the duplicates, cap description length at a reasonable ceiling, and move on. After cleanup, I still had 2,184,483 usable articles, a loss of less than two percent. Good enough to trust.

There's a broader lesson here that applies well beyond journalism datasets. Any time you inherit data, whether it's sales figures, survey responses, or sensor readings, the first hour should be spent asking "does this make sense?" before you ask "what does this mean?" Skipping that step is how confident-sounding conclusions get built on broken foundations.

### The Pulse of a Newsroom, Year by Year

With clean data in hand, the first real question was simple: how much did the Times actually publish, year over year?

**[Insert graph: "The Rise and Fall of NYT Article Volume" — bar chart of articles per year, 2000-2025, with 2006 highlighted as peak and 2022 highlighted as the low point]**

The shape of that chart tells its own story. Article volume climbed steadily through the 2000s, peaked in 2006 at over 163,000 articles, then began a long, mostly uninterrupted decline through the 2010s. By 2022 the dataset shows just under 20,000 articles for the entire year, before recovering somewhat in 2023 through 2025.

Is that decline real? Partly. Some of it reflects a genuine industry shift: newsrooms shrank, and the Times itself moved toward fewer, deeper stories rather than high-volume wire coverage. But the sharpest drop, the cliff around 2021 and 2022, is almost certainly a data collection gap rather than an editorial choice. The API that fed this dataset likely had a period where it wasn't capturing everything. Good data analysis means holding both of those truths at once: a real trend, distorted by a real gap, and knowing you can't always cleanly separate the two from the outside.

I also checked whether certain months of the year get more news than others. My first pass suggested February was unusually quiet, but that turned out to be an illusion: February simply has fewer days than every other month, so of course it has fewer articles. Once I normalized by dividing the article count by the number of days in each month, that illusion disappeared.

**[Insert graph: "When Does The Times Publish Most?" — bar chart of articles by month]**

The corrected version shows something much more interesting: NYT's daily publishing rate is remarkably stable across the calendar, hovering around 6,000 articles a day no matter the month, with only modest dips in July and around the winter holidays. The newsroom, it turns out, doesn't take many days off.

### The Vocabulary of Twenty-Five Years

Once the timeline was in shape, I wanted to know what the Times was actually writing about. The simplest way to find out is to count words.

**[Insert graph: "25 Years of Headlines: What Did The Times Write About?" — lollipop chart of top 25 title words]**

The results were a mix of genuinely revealing and structurally boring. Words like "paid" and "notice" topped the list, but that's not really news coverage, that's the paid obituary section, a recurring feature of the print paper that happened to use consistent boilerplate language in its headlines for two decades. Once I separated those structural words from real content, a clearer picture emerged: "trump," "china," "obama," and "europe" were among the most frequent proper nouns, alongside recurring topical words like "business," "court," and "health."

This is a useful reminder for anyone doing text analysis on real-world data: raw word counts always surface the loudest, most repetitive patterns first, and those are often boring administrative artifacts rather than meaningful signal. You have to actively hunt for and remove the noise before the interesting stuff becomes visible.

### Finding What Made Each Era Different

Counting words tells you what's common. It doesn't tell you what's distinctive. For that, I turned to a technique called TF-IDF, which sounds technical but is actually a pretty intuitive idea once you unpack it.

Imagine two friends describing their week. One says "I ate breakfast and went to work." The other says "I got engaged." The word "engaged" carries far more information than "breakfast," even though breakfast might get mentioned more often across everyone's week, because "engaged" is rare and specific to that moment, while "breakfast" is common and tells you nothing distinctive. TF-IDF is a mathematical way of finding the "engaged" words in a body of text: the ones that spike in one place and stay quiet everywhere else.

I split the 25 years into five eras: Pre-9/11, the War on Terror years, the Obama era, Trump's first term through COVID, and the post-COVID years through 2025. Then I asked which words were distinctively associated with each period.

**[Insert graph: "What Defined Each Era? 25 Years of NYT Headlines" — heatmap of TF-IDF scores by era]**

The results read almost like a history textbook condensed into a single image. "Iraq" lights up brightly during the War on Terror years and then fades to near-zero everywhere else, a word that mattered enormously for seven years and then largely vanished from the front page. "Obama" appears only during his own era, disappearing almost entirely the moment he left office. "Trump" is essentially absent before 2017, then dominates two consecutive eras in a row. And "Ukraine," a word that barely registers for the first twenty-two years of the dataset, suddenly becomes one of the defining terms of the post-COVID period.

One word stood apart from all the others: "China." It's the only term that stays consistently present across every single era, never disappearing, never spiking dramatically, just a steady undercurrent running through 25 years of American news coverage. If you wanted a single word to describe the most durable story of this century so far, that heatmap makes a quiet, compelling case for it.

### Did the News Get Darker? Measuring Tone at Scale

This is where the project got genuinely surprising, and where I also made a mistake worth talking about honestly.

I wanted to know whether the emotional tone of headlines had shifted over 25 years. To do that, I used a sentiment analysis tool that scores text on a scale from very negative to very positive based on the words it contains. Run across every headline in a given year and averaged, you get a rough sense of the emotional temperature of that year's news.

My first version of the chart looked dramatic: 2000 was the only year with a net positive average score in the entire dataset. Every single year after that, the average tilted negative, with the steepest and steadiest decline beginning in 2017 and reaching its lowest point in 2025.

I shared that chart for feedback, and got back a pointed but fair critique: an average, on its own, can be misleading. If you only show the mean sentiment score without showing how much individual headlines vary around that average, you can't tell whether a shift is a real, meaningful trend or just noise that happens to average out in one direction. It's the difference between saying "the average person in this room is 5'9"" and actually showing the range of heights in the room. The average alone hides whether everyone is close to that number or wildly scattered around it.

There was a second, more specific problem too: this kind of sentiment tool is built to score words, not context. A headline like "murder rate falls to ten-year low" contains the word "murder," which reads as strongly negative to the algorithm, even though the actual news is good. Averaged across two million headlines, this kind of misclassification doesn't cancel out cleanly, because certain topics (crime, war, disease) use negative-sounding vocabulary even when reporting genuinely positive developments within those topics.

So I rebuilt the chart with two fixes. First, I added a shaded band around the trend line showing the statistical margin of error for each year's average, so you can see at a glance whether year-to-year differences are big enough to be meaningful or small enough to be noise. Second, I added a plain-language caveat directly onto the chart itself, explaining that the tool measures vocabulary, not necessarily editorial tone.

**[Insert graph: "25 Years of NYT Headlines Got Darker Every Year" — sentiment trend line with shaded error band, final version]**

Even with those honest caveats built in, the underlying trend held up. The shaded band stays tight and low throughout, meaning the downward drift isn't just noise, it's a real and fairly steady pattern. Sentiment dipped sharply after September 11th and never fully recovered to its 2000 baseline. It brightened modestly around Obama's 2008 election. And starting in 2017, it entered a long decline that reached its lowest point of the entire quarter century in 2025.

I want to dwell on this moment for a second, because I think it's more valuable than any single chart in this whole project: the instinct to add uncertainty bands and caveats didn't come from me getting it right the first time. It came from someone checking my work, finding a real weakness, and me being willing to rebuild rather than defend the prettier, less honest version. That's not a failure in a data project. That's the actual job.

### Watching Words Rise and Fall Like a Heartbeat

If the TF-IDF heatmap showed which words defined each era in broad strokes, I wanted one more chart that showed the texture of that story unfolding year by year, almost like a heart rate monitor for the news cycle.

**[Insert graph: "The Words That Defined the News Cycle: 2000-2025" — bump chart tracking ten key terms over time]**

Tracking ten specific terms (Iraq, Bush, Obama, Trump, COVID, China, Ukraine, Biden, police, election) normalized by how many articles were published that year, the resulting chart looks almost like a seismograph. "Iraq" spikes sharply in 2003 and gradually flatlines over the following decade. "Obama" rises cleanly through his two terms and drops off almost immediately after he leaves office. "COVID" appears from nowhere in 2020, dominates briefly, and fades. And then there's "Trump," whose line does something none of the others do: after an initial surge in 2017, it dips slightly, then explodes upward again in 2024 and 2025, ending the chart at roughly 1,500 mentions per 10,000 articles, by far the single most concentrated presence of any word, person, or topic across the entire 25-year dataset.

That last point deserves a caveat of its own, because it's the kind of thing that trips up even experienced analysts. A separate chart later in this project, showing raw mention counts of specific people extracted from the text, actually shows former President Bush with more total mentions than Trump across the full dataset. That's not a contradiction, it's two different questions getting two different honest answers. Bush accumulated more total mentions because he was president during years when the Times published far more articles overall, over 100,000 a year. Trump's mentions are more concentrated because he dominates years when the paper published fewer articles overall, but he dominates them completely. One measures total volume, the other measures share of attention within an era. Both are true. Neither is more "correct" than the other; they're just answering different questions, and knowing which question you're actually asking is half the battle in any kind of data work.

### Teaching a Computer to Recognize Names, and Where It Gets Confused

The last major piece of analysis involved a technique called Named Entity Recognition, or NER, which is exactly what it sounds like: teaching a program to scan text and pull out the names of real people, places, and organizations, the same way a human reader would instinctively recognize "Iraq" as a country and "Bush" as a person without needing to be told.

**[Insert graph: "Who and What Did The Times Cover? 25 Years of Named Entities" — three-panel bar chart of top people, places, and organizations]**

Run across a stratified sample of 400,000 headlines, the results surface a fairly intuitive who's who of the era: Bush, Clinton, Trump, and Obama dominate the people extracted, the United States, China, and Iraq dominate the places, and Congress, the United Nations, and the White House dominate the organizations. Encouragingly ordinary, and mostly reassuring, since it means the underlying method is working the way it should.

But two names on that list forced an honest conversation about a real limitation of this kind of analysis, and I think it's worth walking through because it applies to any project involving names, not just this one.

The name "Clinton" appears throughout the dataset, but it could refer to two different people: Bill Clinton, who was president when this dataset begins in 2000, or Hillary Clinton, who became a prominent figure in her own right as Secretary of State and later as a presidential candidate. A computer reading the bare word "Clinton" out of context has no reliable way to know which one is meant, especially in years where both were making headlines simultaneously.

The same problem shows up with "Trump." Before 2015, the word overwhelmingly referred to the Trump real estate and hospitality brand: Trump Tower, Trump Hotels, Trump Organization deals. After 2015, it almost entirely refers to the man himself as a political figure. A simple word count can't tell those two meanings apart on its own.

There were a couple of ways to handle this. I could have tried to guess, using the article's publication year as a rough signal (Clinton mentioned before 2007 is probably Bill, after 2015 probably Hillary), but that guess would be wrong often enough in the murky years between to be misleading if I presented it as fact. Instead, I chose the more honest path: I merged the ambiguous names together in the chart and added a clear, visible footnote explaining exactly what was combined and why, so that anyone reading the chart understands its limits rather than being quietly misled by false precision.

This might be the most practically useful lesson of this entire project for anyone starting out in data analysis. It is almost always more valuable, and more credible, to clearly show the limits of what your data and methods can tell you than to paper over that uncertainty with a chart that looks cleaner than the truth actually is. A slightly messier, more honest chart will always outperform a beautifully polished one built on a hidden assumption, once someone finds the seam.

### What a Quarter Century of Headlines Actually Told Me

Stepping back from the individual charts, a few big-picture takeaways stayed with me after this project.

The tone of the news really has shifted, and not subtly. Twenty-five years of headlines contain exactly one year, the very first one, with a net positive emotional register on average. Every year since has leaned negative, with the decline accelerating sharply after 2017 and hitting its lowest point in the most recent year measured. Even accounting for the real limitations of automated sentiment scoring, that's a striking, sustained pattern, not a blip.

Attention is a finite, contested resource, and the data shows exactly how it gets redistributed. Iraq owned a chapter of the news cycle for roughly seven years and then all but disappeared. Obama owned eight years and vanished from the front page almost the moment he left office. COVID arrived instantly and dominated completely, then faded fast. Only one subject, China, managed to stay present through every single era without ever fully commanding the spotlight or fully leaving it. That kind of quiet persistence turned out to be rarer, and in its own way more remarkable, than any single dramatic spike.

And maybe the most transferable lesson: the gap between a chart that looks convincing and a chart that is actually trustworthy is usually invisible until someone checks your work. The most important thing I did in this entire project wasn't picking the right sentiment tool or the cleverest visualization technique. It was rebuilding a chart I already liked, after someone pointed out a real flaw in it, rather than defending the version that looked better but told a less honest story.

If there's one habit worth taking from a project like this, whether you ever touch a line of Python or not, it's that instinct: before you trust a number, ask what it's hiding. Before you trust a trend, ask what happens if you zoom out or normalize for something you hadn't considered. And before you publish a conclusion, ask whether you'd still believe it if someone smarter than you spent twenty minutes trying to poke a hole in it.

Twenty-five years of headlines can tell you a lot about a country's mood. But the real skill isn't extracting the story. It's knowing which parts of that story you can actually trust, and being honest about the parts you can't.

---

*This analysis was built entirely in a Google Colab notebook using Python, pandas, spaCy, and NLTK's VADER sentiment tool, on a public New York Times headline dataset spanning 2000 to 2025. All charts were custom-built in Matplotlib.*
