# MedQA-BBY

MedQA-BBY (MedQA-but-better-yield) significantly enhances the original MedQA dataset, addressing crucial limitations in medical question-answering systems. Our motivation stems from the inherent complexity of medicine, where:

1. Multiple correct answers often exist for a single question
2. Incorrect answers vary in their potential impact on patient care (some can harm patient)
3. Creating open-ended questions is hard for evaluation (even with embedding models)

Key Improvements:

1. Refined Answer Structure:
   • Two correct options (reflecting real-world medical scenarios with multiple valid approaches)
   • One negative-point option (representing potentially harmful choices)
   • Three zero-point options (incorrect but not directly harmful)

2. Comprehensive Labeling System:
   • Question categorization (anatomical system, medical discipline, subspecialty)
   • Linguistic metrics (token length)
   • Educational assessment (Bloom's Taxonomy classification)

This enhanced dataset aims to evaluate Large Language Models (LLMs) in a manner that more accurately reflects real-world medical practice, moving beyond the limitations of the previous single-best-answer approach. By doing so, MedQA-BBY provides a more nuanced and practical tool for assessing and developing AI systems in healthcare.

# Term of use
Please cite the original MedQA paper ([Jin, Di, et al. "What Disease does this Patient Have? A Large-scale Open Domain Question Answering Dataset from Medical Exams." arXiv preprint arXiv:2009.13081 (2020)](https://arxiv.org/abs/2009.13081)) and our forthcoming paper (to be published on arXiv). Our team, composed of medical graduates from Iran, has built upon this  work. Lastly, I have a brief message I'd like to share:

> History teaches us that isolation breeds conflict. World War II, a catastrophe of unprecedented scale, was partly fueled by the alienation of entire nations. Today, we risk repeating this grave error. Sanctions, while a tool of international diplomacy, can be a double-edged sword when they indiscriminately affect millions of innocent lives.
> 
> Consider Iran, a nation of 80 million souls. When we deny these people access to global platforms, delay their visa applications without explanation, or infringe upon their basic rights, we don't just isolate a government – we alienate an entire populace. This approach doesn't weaken extremist leaders; it strengthens them by fomenting anger and resentment among ordinary citizens.
> 
> Imagine the frustration and helplessness of being unable to find your country listed on a simple website. This daily indignity is the reality for millions of Iranians. While not all sanctions are inherently flawed, when we sever the connections between people and the wider world, we sow the seeds of future conflicts rather than resolve current ones.
> 
> Our challenge, then, is to craft a world for our children where peace is not a distant aspiration, but a carefully cultivated reality. This requires us to recognize the humanity in all people, even those whose governments we oppose. May our children inherit a world where peace is not just a dream, but a reality we've worked tirelessly to create.

# Special thanks

- Thanks to Jin Di et al. for providing the MedQA dataset ([paper](https://arxiv.org/abs/2009.13081), [github](https://github.com/jind11/MedQA?tab=readme-ov-file))
- Thanks to the Streamlit team for making life easier for developers
- Thanks to our team for dedicating their time to crafting this dataset

# Team Zone

- Link to the app: [MedQA-BBY-app](https://medq-bby-app.streamlit.app/) 
- Link to [Google sheet and assigned batch for each person](https://docs.google.com/spreadsheets/d/1_NK8wMHkDgLfEx6VB_BY6YSvXpMQ_ls6Xzlai2h3pJ4/edit?usp=sharing)
- Instruction (...loading)
