# Examining the Impact of Generative AI on Undergraduate Academic Performance Across Disciplines at UCSD

## Introduction
With the rapid advancements in generative AI technologies like OpenAI's ChatGPT, the educational landscape is undergoing significant transformations. This project aims to examine the impact of these AI tools on undergraduate academic performance at UC San Diego by analyzing the distributions of average grades received before and after their introduction. By focusing on both Arts and STEM disciplines, we seek to uncover any possible trends or disparities in academic outcomes. The relevance of this study lies in its potential to guide educators, policymakers, and technology developers in ethically integrating AI into educational environments. By analyzing data from UCSD's Course and Professor Evaluations (CAPE) database, we hope to provide valuable insights into the evolving role of AI in higher education.

## Data
### Data Source
The primary data source for this project is the Course and Professor Evaluations (CAPE) database, a student-run organization that administers standardized evaluations of UCSD's undergraduate courses and professors. CAPE collects student feedback to gauge the quality of the University's curriculum and faculty, providing insights into the opinions of students on specific courses and professors.

To acquire the data, we followed CAPE's recommendation to download the webpage and extract data directly from the HTML. We focused on courses from the following departments: BILD, CHEM, CSE, ECE, ENG, MATH, and PHYS for STEM courses, and LT, MUS, PHIL, and VIS for Arts courses.

A full data description can be found in appendix.

### Preprocess
The preprocessing phase involved several key steps. Firstly, we handled missing values by dropping courses that did not have an average grade due to reasons such as offering only pass/no pass options. Next, we tagged courses as "pre-GPT" if they were before 2022 and "post-GPT" if they were after 2022 (inclusive). Additionally, we divided STEM courses into abstract courses (proof-based or focusing on abstract concepts) and non-abstract courses, and Arts courses into written material-based and non-written material-based. Such division is based on the ability of GPT being limited when it is facing proof-based or abstract concepts, and it has no capability to recognize images and audio to the time of data cutoff. Each course was also tagged as either an upper division or a lower division course. This meticulous preparation ensured that our subsequent analyses would be robust and meaningful, providing accurate insights into the impact of generative AI on academic performance.

In order to automate and speed up the process, we use LLM to identify abstract courses. Details can be found in appendix.

### Data Limitations
It is important to note that CAPE stopped publishing data after the Fall 2023 semester, so our analysis is limited to data up until that point. Although we considered using an alternative resource, the SunSET dataset, we found it impossible to distinguish fake data within it, leading us to abandon its use.

## Exploratory Data Analysis (EDA)
Pending

## Proposed Analysis
### Assumptions
To ensure the validity of our analysis, we made the following assumptions:
- The average grades received before the introduction of GPT (pre-GPT) and after the introduction of GPT (post-GPT) follow a normal distribution:
  $$
  \bar{X}_{course, pre-GPT} \sim N(\mu_{course, pre-GPT}, \sigma^2_{course, pre-GPT})
  $$
  $$
  \bar{X}_{course, post-GPT} \sim N(\mu_{course, post-GPT}, \sigma^2_{course, post-GPT})
  $$

### Subgroup divisions
To facilitate a detailed and meaningful analysis, we divided the courses into several subgroups based on the following criteria:
- *Course Level*: Upper division or lower division
- *Discipline*: STEM or Arts
  - *STEM Courses*:
    - Abstract (proof-based or focusing on abstract concepts)
    - Non-abstract
  - *Arts Courses*:
    - Written material-based
    - Audio/visual material-based

### Methods Used
Each subgroup will undergoes the following analytical methods to compare the distributions of average grades received before and after the introduction of GPT:
1. Visualization of distribution<br>
    We will plot histograms and box plot to give a preliminary review of the distribution
2. Welch's t-test with bootstrapping<br>
    Because it is not reasonable to assume equal variance, we use Welch's t-test to check if the mean of average grade received before and after the introduction of GPT is the same. That is to say, for each subgroup, we have:
    $$
    H_0: \mu_{\text{pre-GPT}} = \mu_{\text{post-GPT}}\\
    H_1: \mu_{\text{pre-GPT}} \neq \mu_{\text{post-GPT}}
    $$
    Additionally, due to the shorter duration of the post-GPT era, we will use bootstrapping methods to balance the number of samples between pre-GPT and post-GPT data.

    Implementation details of bootstrapped t-test can be found in appendix
    
## Results
For each subgroup, we simulate the bootstrapped two-sampled t-test 1000 times. In each simulation, the bootstrap process is repeated for 1000 times. The seed for `numpy` random seed generator is set to be 189.

### STEM

## Comparative Analysis
Pending

## Limitations
Pending

## Conclusion
Pending

## Appendix
### Data Description
#### Features
CAPE provides following features:
- Instructor: *Name of the instructor*
- Course: *Name of the course,*
- Term: *In which term the course is held*
- Enroll: *Number of students enrolled*
- Evals Made: *Number of evaluations made (does not affect Avg Grade Expected)*
- Rcmnd Class: *Proportion of students who recommend class*
- Rcmnd Instr: *Proportion of students who recommend instructor*
- Study Hrs/wk: *Study hours per week*
- Avg Grade Expected: *Expected average grade (among evaluations made)*
- Avg Grade Received: *Actual average grade (among all students)*

As described in the preprocess section, we introduced following new features to our dataset:
- isPreGPT: *Inidicating if the course is taught before ChatGPT is introduced*
- isUD: *Indicating if the course is an upper-division course*
- isSTEM: *Indicating if the course is a STEM course*
- isAbstract: *The course is either proof based or focusing on abstract concepts that GPT is not good at (valid if `isSTEM=True`)*
- isWritten: *The course is mainly based on written materials instead of audio/video (valid if `isSTEM=False`)*

#### Number of Samples
Before preprocessing, there are 23363 samples. 8255 samples are from Arts courses and 15108 samples are from STEM courses.

After preprocess, there are 15463 samples. 4648 samples are from Arts courses and 10815 samples are from STEM courses. 13571 samples are tagged as "pre-GPT" and 1892 samples are tagged as "post-GPT."

Among 4648 samples from Arts courses, 2462 courses are tagged as "written based" and 2186 courses are tagged as not.

Among 10815 samples from STEM courses, 806 courses are tagged as "abstract" and 10805 courses are tagged as not.

#### Additional Note
CSE 20 is excluded from this analysis because it is the only proof-based lower division course. It is not reasonable to merge it into any subgroup of STEM courses.

### Usage of LLM
We craft part of the UCSD catalog information into the following prompt:
> Abstract courses are defined as courses that are either proof-based or focusing on abstract concepts. Please go over the following catalog and identify which courses are abstract:<br>
> \###<br>
> \<catalog><br>
> \###<br>
> Please take a deep breath and explain your choice.

The prompt is then sent to ChatGPT-3. In order to avoid dependency issues, the length of each request is controlled to be under 700 words. (i.e. roughly lower than 1000 tokens) The result will be reviewed by human to make sure there is no false positive. However, please be aware that there might still be false negatives. (i.e. abstract courses might be classified as non-abstract courses)

### Bootstrapped Two-sampled T-test
The bootstrapped two-sampled t-test is defined as follows:
1. Find the t-statistic on the original data
2. Mix the data together
3. Perform bootstrapping on the mixture of data. The parameter of interest is mean
4. Find the t-statistic on the bootstrapped result
5. Repeat step 3 and 4 for desired number of times
6. Find the p-value using following formula:
    $$
    \frac{\text{number of (bootstrapped t-statistic > original t-statistics)}}{\text{number of trails}}
    $$
Note that only the first step might need Welch's t-test depending on the data. Additionally, if we are doing a two-sided test, we need to use absolute value of obsered t-statistics and bootstrapped t-statistics instead of their original value.

This method is inspired by Algorithm 16.1 described in Chapter 16 of An Introduction to the Bootstrap by Bradley Efron and Robert J. Tibshirani. The original algorithm is defined as follows:
1. Draw $B$ samples of size $n+m$ with replacement from $x$. Call the first $n$ observations $z^*$ and the remaining $m$ observations $y^*$
2. Evaluate $t(\cdot)$ on each sample,
    $$
    t(x^{*b})=\bar z^* - \bar y^*,\ \ b\in\{1,2,..., B\}
    $$
3. Approximate $\text{ASL}_{\text{boot}}$ by
    $$
    \widehat{\text{ASL}}_{\text{boot}} = \#\{t(x^{*b})\geq t_{obs})\}/B
    $$
    where $t_{obs}$ is the observed value of the statistic

Although the proposed bootstrapped two-sampled t-test keeps the structure proposed by Bradley and Robert, it is still hard for us to justify why mixing data with different variance and treat the new mixed data as equal variance works (i.e. step 3 and step 4). However, it is possible for us to demonstrate the distribution of p-values under null hypothesis is indeed $\text{Uniform}(0,1)$ via simulation.

#### Simulation 1 Setup
We set the seed of `numpy` random number generator to be 42. For each simulation, we sample 30 samples from $N(0,1)$ as $\textbf{x}$ and 300 samples from $N(0,1)$ as $\textbf{y}$. Absolute values are used to demonstrate a two-sided test. The null hypothesis is:
$$
H_0: \bar{\textbf{x}}=\bar{\textbf{y}}
$$
Bootstrapping process is repeated for 1000 times for each simulation. After 1000 simulations, the distribution of $p-values$ is shown below:
![alt text](image.png)

#### Simulation 2 Setup
We set the seed of `numpy` random number generator to be 42. For each simulation, we sample 30 samples from $N(0,1)$ as $\textbf{x}$ and 300 samples from $N(0,16)$ as $\textbf{y}$. Absolute values are used to demonstrate a two-sided test. The null hypothesis is:
$$
H_0: \bar{\textbf{x}}=\bar{\textbf{y}}
$$
Bootstrapping process is repeated for 1000 times for each simulation. After 1000 simulations, the distribution of $p-values$ is shown below:
![alt text](image-1.png)

#### Simulation 3 Setup
We set the seed of `numpy` random number generator to be 42. For each simulation, we sample 30 samples from $N(0,1)$ as $\textbf{x}$ and 300 samples from $N(0,1)$ as $\textbf{y}$. Absolute values are ***not*** used to demonstrate a one-sided test. The null hypothesis is:
$$
H_0: \bar{\textbf{x}}=\bar{\textbf{y}}
$$
Bootstrapping process is repeated for 1000 times for each simulation. After 1000 simulations, the distribution of $p-values$ is shown below:
![alt text](image-2.png)