## AnalyticsCapstone
### Problem/Opportunity:
During congressional negotiations over the details of the Consolidated Appropriations Act, 2021 (HR 133), there was a media frenzy over the length (5,593 pages) and details of the bill. This narrative was centered around the impossible task of reading the bill in its entirety before representatives were expected to vote on its approval. Many voters are skeptical of government spending and the bundling of unrelated issues into single bills. By programmatically summarizing these lengthy bills, representatives can gain greater transparency into the issues they are voting on, and voters can better hold elected officials responsible for accurately representing the interests of their constituents. 

### Goal:
Identify, define, and implement metrics for congressional bills that will provide an accurate summary of the bill details. These metrics can then be used to target specific areas of the bill that warrant a further suitability review.

### Objectives:
- Produce a value:recipient mapping of all spending directives proposed in the bill by scanning the text and parsing the financial allocation and recipient pairings. Every recipient of proposed funding should be identified.
- Produce a most and least prevalent keyword cloud by tokenizing the text, counting frequencies, and identifying keywords. The most prevalent keywords should be closely related to the topic of the bill; the least prevalent keywords should be least related to the topic of the bill.
- Produce a suitability score for the bill that represents how closely the bill details represent the original intent by comparing deviations between the keyword clouds and spending summary. Additionally, this will include a listing of the sections in the bill that are most negatively impacting the suitability score.

### Success Criteria:
By mid-April 2021, objectives 1) and 2) will be accurate and reproducible on all modern congressional legislation that is published and objective 3) will be subjectively accurate for at least three test examples. The outputs of these summary metrics will be able to be displayed in a text format and visual dashboard. Users will be able to view the summary and make an informed decision on whether to support/reject the bill or do a deeper investigation into specific sections without being required to read every page.

### Assumptions, Risks, Obstacles:
- ***A/R 1:*** An assumption is being made that all documents are formatted and written in a standard legal format and with specific legalese. If similar wording and formatting standards are not used across different documents, this will pose a significant risk to the accuracy of the metrics. Ex: “no(t) less than {financial amount} shall be available for {program}”
- ***A/R 2:*** An assumption is being made that most bills are focused on a specific topic. If a number of large themes are addressed in one bill, this increases the risk that the accuracy of the metrics will not properly represent the high-level theme. Ex: The CARES Act was specifically targeted towards COVID-19 relief whereas the Consolidated Appropriations Act, 2021 was a combined spending bill for COVID-19 relief and the 2021 fiscal year omnibus spending budget. 
- ***A/R 3:*** An assumption is being made that the govinfo.gov bulk data repository can be used to collect all legislative bills for a specific time-frame. If this is not true, documents will need to be collected manually. A smaller set of documents to train on increases the risk that the metrics will not be accurate for a wide number of bills that were not trained on. 
- ***Obstacle 1:*** I do not have much experience doing natural language processing. I will need to learn NLP best practices and libraries while actively working on the project.
- ***Obstacle 2:*** Standard NLP libraries are not tailored for legal writing. Extensive adjustments to the stop-word and supplemental libraries may be required.
