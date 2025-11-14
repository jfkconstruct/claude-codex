# Data Science Domain: Claude Implementation Patterns

*Last Updated: 2025-11-14*

## Overview

Claude Code is transforming data science workflows through code generation, debugging assistance, data analysis automation, and SQL query creation. With the ability to work across Python, R, SQL, and various data science libraries, Claude demonstrates strong capabilities for data manipulation, exploratory analysis, statistical modeling, and generating production-ready code.

---

## Table of Contents
1. [Compliance Considerations](#compliance-considerations)
2. [Unique Prompting Strategies](#unique-prompting-strategies)
3. [Specialized Patterns](#specialized-patterns)
4. [Success Metrics](#success-metrics)
5. [Case Studies](#case-studies)
6. [Implementation Guidance](#implementation-guidance)

---

## Compliance Considerations

### Data Privacy & Security

**Sensitive Data Protection:**
- **PII (Personally Identifiable Information)**: Remove before analysis when possible
- **PHI (Protected Health Information)**: HIPAA compliance requirements
- **PCI (Payment Card Industry)**: Credit card data protection
- **Proprietary data**: Client confidential information, trade secrets
- **GDPR/CCPA**: EU and California privacy regulations

**Best Practices:**
- **De-identification**: Remove or mask identifiable information
- **Synthetic data**: Use for testing and development
- **Data minimization**: Only include necessary fields in prompts
- **Secure environments**: Use appropriate deployment options
- **Access controls**: Role-based permissions for data access

### Code Security & Quality

**Security Considerations:**
- **SQL injection**: Validate AI-generated SQL for injection vulnerabilities
- **Code review**: Always review generated code before production deployment
- **Dependency safety**: Check AI-recommended packages for security issues
- **Credential management**: Never include API keys, passwords in prompts
- **Data validation**: Ensure proper input sanitization

**Quality Assurance:**
- **Testing**: Validate AI-generated code with test cases
- **Documentation**: Ensure code is well-commented and maintainable
- **Performance**: Check for inefficient or resource-intensive operations
- **Reproducibility**: Set random seeds, document environment
- **Version control**: Track AI-assisted code changes

### Intellectual Property

**Code Ownership:**
- **Generated code**: Understand licensing and ownership
- **Proprietary algorithms**: Protect company IP in prompts
- **Open source**: Ensure AI doesn't replicate copyrighted code
- **Attribution**: Document AI assistance for transparency

---

## Unique Prompting Strategies

### Data Analysis Workflows

**Comprehensive Data Analysis:**
```
Role: Data scientist conducting exploratory data analysis (EDA).

Dataset: [Description or file path]
Format: [CSV / Excel / JSON / Database / API]

Business context:
- Domain: [Industry or application]
- Goal: [What insights are needed]
- Key questions: [Specific business questions]

Data analysis tasks:
1. Data Loading & Inspection:
   - Load data with appropriate error handling
   - Display shape, column names, data types
   - Check for missing values
   - Identify potential data quality issues

2. Data Cleaning:
   - Handle missing values (strategy: [drop / impute / flag])
   - Fix data type issues
   - Remove duplicates
   - Standardize formatting
   - Handle outliers

3. Exploratory Data Analysis:
   - Summary statistics (mean, median, std, quartiles)
   - Distribution analysis (histograms, box plots)
   - Correlation analysis (heatmap)
   - Identify patterns and anomalies
   - Time series trends if applicable

4. Visualizations:
   - Use [matplotlib / seaborn / plotly]
   - Create [specific chart types]
   - Professional styling and labels
   - Save figures to [path]

5. Key Insights:
   - Answer specific business questions
   - Flag notable patterns or anomalies
   - Suggest further analysis or modeling
   - Present findings clearly for stakeholders

Code requirements:
- Well-commented and organized
- Use pandas, numpy, scikit-learn as appropriate
- Include error handling
- Make reproducible (set random seeds)

Output: Jupyter notebook or Python script with analysis and visualizations.
```

**Statistical Modeling:**
```
Role: Data scientist building statistical or machine learning model.

Data: [Dataset description]
Target variable: [What we're predicting]
Features: [Available predictors]

Modeling objective: [Classification / Regression / Clustering / Time series]

Modeling workflow:
1. Data Preprocessing:
   - Train/test split (or time-based split for time series)
   - Feature engineering
   - Encoding categorical variables
   - Scaling/normalization
   - Handle class imbalance if applicable

2. Model Selection:
   - Try multiple algorithms: [list candidates]
   - Use appropriate evaluation metrics: [accuracy / RMSE / AUC / etc.]
   - Cross-validation strategy

3. Model Training:
   - Train candidate models
   - Hyperparameter tuning (grid search or random search)
   - Track metrics for comparison

4. Model Evaluation:
   - Performance on test set
   - Confusion matrix (classification)
   - Feature importance
   - Residual analysis (regression)
   - Model assumptions validation

5. Model Interpretation:
   - Which features drive predictions?
   - Model limitations and caveats
   - Recommended next steps

Libraries: pandas, scikit-learn, [xgboost/lightgbm if applicable]

Output: Trained model, evaluation metrics, interpretation, and production-ready code.
```

### SQL & Database Operations

**Natural Language to SQL:**
```
Role: Data analyst translating business questions to SQL queries.

Database context:
- Database type: [PostgreSQL / MySQL / SQL Server / Snowflake]
- Schema: [Table structures, relationships]
- Key tables: [Names and descriptions]

Business question: [Natural language query]

SQL generation requirements:
1. Translation Process:
   - Break down business question into logical steps
   - Identify relevant tables and joins
   - Determine necessary filters, aggregations
   - Explain reasoning for query structure

2. Query Generation:
   - Write initial SQL query
   - Review and refine for accuracy
   - Optimize for performance if needed
   - Include comments explaining logic

3. Query Validation:
   - Check for common errors (syntax, joins, aggregation)
   - Verify it answers the original question
   - Consider edge cases

4. Query Optimization:
   - Use appropriate indexes if available
   - Avoid unnecessary subqueries
   - Optimize join order
   - Limit result set appropriately

Output:
- Well-structured SQL query
- Explanation of query logic
- Expected result format
- Performance considerations

Best practice: Instruct Claude to break down steps and show reasoning
for more understandable SQL.
```

**Database Analysis & Schema Understanding:**
```
Role: Database analyst exploring and understanding database structure.

Database: [Connection details or schema description]

Tasks:
1. Schema Documentation:
   - List all tables with descriptions
   - Document column names, types, constraints
   - Identify primary and foreign keys
   - Map table relationships (ERD-style)

2. Data Profiling:
   - Row counts per table
   - Column cardinality (distinct values)
   - Missing value analysis
   - Data type consistency
   - Identify potential data quality issues

3. Query Patterns:
   - Common join patterns
   - Frequently queried dimensions
   - Aggregation examples
   - Sample analytical queries

4. Optimization Recommendations:
   - Suggested indexes
   - Denormalization opportunities
   - Partitioning strategies
   - Query performance improvements

Output: Comprehensive database documentation with analysis and recommendations.
```

### Code Generation & Refactoring

**Python Code Generation:**
```
Role: Data scientist writing production-quality Python code.

Task: [Specific data science task]
Language: Python [version]
Libraries: [pandas, numpy, scikit-learn, etc.]

Code requirements:
1. Functionality:
   - [Specific operations needed]
   - Handle edge cases
   - Input validation
   - Error handling

2. Code Quality:
   - Clear variable names
   - Comprehensive docstrings
   - Type hints
   - Follow PEP 8 style guide
   - Modular functions (single responsibility)

3. Performance:
   - Efficient algorithms and data structures
   - Vectorized operations where possible
   - Avoid unnecessary loops
   - Memory-efficient for large datasets

4. Testing:
   - Include unit tests (pytest)
   - Test edge cases
   - Validate outputs
   - Include example usage

5. Documentation:
   - Module/class/function docstrings
   - README with usage examples
   - Comment complex logic
   - Specify dependencies

Output: Production-ready code with tests and documentation.
```

**Code Debugging & Optimization:**
```
Role: Debugging assistant for data science code.

Code: [Paste problematic code]
Error: [Error message or description of issue]
Expected behavior: [What should happen]

Debugging approach:
1. Error Analysis:
   - Identify root cause
   - Explain why error occurs
   - Point to specific problematic lines

2. Solution:
   - Provide corrected code
   - Explain what was fixed
   - Suggest best practices to avoid similar issues

3. Optimization (if applicable):
   - Identify performance bottlenecks
   - Suggest more efficient approaches
   - Compare time/space complexity

4. Testing:
   - Suggest test cases to validate fix
   - Identify edge cases to handle

Claude advantage: More efficient debugging than traditional trial-and-error,
particularly for pandas operations, numpy manipulations, or scikit-learn
pipeline configurations.

Output: Debugged code with explanation and testing recommendations.
```

### Data Visualization

**Visualization Creation:**
```
Role: Data visualization specialist.

Data: [Dataset or summary statistics]
Visualization purpose: [Exploratory / Explanatory / Dashboard]
Audience: [Technical / Executive / General]

Visualization requirements:
1. Chart Selection:
   - Choose appropriate chart type for data and message
   - Consider: [bar / line / scatter / heatmap / etc.]
   - Justify choice

2. Implementation:
   - Library: [matplotlib / seaborn / plotly / altair]
   - Professional styling
   - Clear labels, title, legend
   - Appropriate color scheme (consider colorblind-friendly)
   - Proper axis scaling

3. Interactivity (if applicable):
   - Hover tooltips
   - Zoom/pan functionality
   - Filters or selections
   - Responsive design

4. Best Practices:
   - Maximize data-ink ratio
   - Avoid chart junk
   - Tell clear story
   - Accessible design

Code output:
- Complete visualization code
- Customization options documented
- Export functionality (PNG, SVG, HTML)

Example: Generate matplotlib/seaborn/plotly visualizations with professional
styling for data presentations.
```

---

## Specialized Patterns

### Pattern: CLAUDE.md for Project Context

**Problem**: AI needs deep project context for relevant suggestions.

**Solution**: Maintain detailed CLAUDE.md file in project root.

**CLAUDE.md Structure:**
```markdown
# Project: [Name]

## Overview
[High-level project description and goals]

## Data Sources
- [Source 1]: [Description, location, update frequency]
- [Source 2]: [Description, format, access method]

## Project Structure
```
project/
├── data/           # Raw and processed data
├── notebooks/      # Jupyter notebooks for exploration
├── src/            # Source code
│   ├── data/       # Data loading and preprocessing
│   ├── features/   # Feature engineering
│   ├── models/     # Model training and evaluation
│   └── utils/      # Utility functions
├── tests/          # Unit tests
└── docs/           # Documentation
```

## Key Conventions
- Coding style: PEP 8, black formatting
- Branch naming: feature/description, bugfix/description
- Commit message format: [verb] [description]

## Data Dictionary
[Column names and descriptions for key datasets]

## Analysis Goals
[What questions we're trying to answer]

## Dependencies
[Key libraries and versions]

## Common Tasks
[Frequently performed operations with examples]
```

**Usage**:
When prompting Claude, reference CLAUDE.md using @filename syntax for comprehensive project context.

**Benefit**: Claude provides project-specific, contextually appropriate suggestions rather than generic advice.

### Pattern: Iterative Data Analysis Pipeline

**Workflow:**
```
Stage 1 - Initial Exploration:
Prompt: Load [dataset] and perform initial EDA.
Review: Examine outputs, identify data issues

Stage 2 - Data Cleaning:
Prompt: Based on EDA findings, clean data addressing:
  - [Specific issue 1]
  - [Specific issue 2]
Review: Validate cleaning logic

Stage 3 - Feature Engineering:
Prompt: Create features for [target variable]:
  - [Feature type 1]
  - [Feature type 2]
Review: Check feature distributions, correlations

Stage 4 - Modeling:
Prompt: Build [model type] for [prediction task]
Review: Evaluate metrics, interpret results

Stage 5 - Refinement:
Prompt: Based on model results, improve by:
  - [Adjustment 1]
  - [Adjustment 2]
Review: Compare performance

Pattern: Iterative loop over pending tasks, moving completed items
to completed tasks list.
```

**Benefit**: Maintains focus and control over complex multi-stage analyses.

### Pattern: SQL Query Explanation & Refinement

**Two-Stage SQL Process:**
```
Stage 1 - Initial Query:
Prompt: Write SQL query to [business question].
Include reasoning: Break down translation from question to SQL.

Stage 2 - Review & Refine:
Prompt: Review this SQL query:
[Generated query]

Verify:
- Does it answer the original question?
- Are joins correct?
- Is aggregation logic sound?
- Are there performance issues?
- Any edge cases missed?

Refine query based on review.

Result: More accurate and relevant SQL through iterative refinement.
```

**Research Finding**: Prompting Claude to show reasoning improves SQL quality and understandability.

### Pattern: Data Analysis from Diverse Sources

**Problem**: Data comes from multiple formats (CSV, Excel, JSON, databases, APIs).

**Claude Capability**: Works with various data formats seamlessly.

**Implementation:**
```
Data sources for analysis:
1. CSV files: [paths]
2. Excel spreadsheets: [files and sheet names]
3. JSON data: [files or API endpoints]
4. Database: [connection details, tables]
5. API: [endpoints, authentication]

Task: Integrate data from all sources for analysis.

Steps:
1. Load from each source with appropriate error handling
2. Standardize formats and schemas
3. Merge/join as needed
4. Perform unified analysis
5. Handle source-specific issues (e.g., Excel date formatting)

Output: Clean, integrated dataset ready for analysis with
documentation of data lineage.
```

### Pattern: End-to-End Data Pipeline Creation

**Comprehensive Pipeline:**
```
Pipeline components:
1. Data Ingestion:
   - Load from [sources]
   - Initial validation
   - Raw data storage

2. Data Cleaning:
   - Handle missing values
   - Fix data types
   - Remove duplicates
   - Validate business rules

3. Feature Engineering:
   - Create derived features
   - Encoding categorical variables
   - Scaling numerical features
   - Time-based features

4. Model Training:
   - Train/validation/test split
   - Model selection and training
   - Hyperparameter tuning
   - Model persistence

5. Model Deployment:
   - Load trained model
   - Prediction API or batch scoring
   - Monitoring and logging

6. Monitoring & Maintenance:
   - Data drift detection
   - Model performance tracking
   - Retraining triggers

Claude Code advantage: Generate file loading with error handling,
data validation checks, and preprocessing pipelines in seconds.

Output: Complete, production-ready data pipeline with tests and documentation.
```

---

## Success Metrics

### Quantitative Performance Metrics

#### Code Quality & Accuracy

**Benchmark Performance:**
- **SWE-bench (Claude Opus 4)**: **72.5%** pass rate on full dataset
- **SWE-bench (Claude Sonnet 4)**: **72.7%** pass rate
- **Comparison**: GPT-4.1 achieves ~54-55% on same benchmark
- **Snowflake DDL**: Generated code passes all validation checks **without errors on first deployment**
- **Cortex Analyst**: Semantic model succeeded in **exactly two iterations**

**Code Generation:**
- **First-deployment success**: Comprehensive technical solutions delivered in one cycle
- **Debugging reduction**: Eliminates dozens of debugging iterations vs. traditional AI assistants
- **Execution accuracy**: Fundamental shift from assistance to genuine development partnership

#### Efficiency & Productivity

**Time Savings:**
- **Debugging**: More efficient than traditional trial-and-error
- **Code generation**: Seconds for file loading, data validation, preprocessing pipelines
- **Workflow acceleration**: Focus on analysis rather than boilerplate code
- **One-cycle solutions**: No extensive debugging iterations for complex integrations

**Development Workflow:**
- **Initial solutions**: Production-ready code in first attempt (many scenarios)
- **Iteration reduction**: Dramatically fewer debugging cycles
- **Complexity handling**: Successfully tackles complex integrations immediately

### Qualitative Success Indicators

**Developer Experience:**
- **"Genuine development partnership"**: Not just assistance, but collaborative development
- **Confidence**: Trust in generated code reduces need for extensive validation
- **Focus**: More time on analysis and insights, less on implementation details
- **Learning**: Code explanations and documentation improve developer knowledge

**Code Characteristics:**
- **Reliability**: Consistently generates working code
- **Maintainability**: Well-structured, documented, and readable
- **Best practices**: Follows language idioms and conventions
- **Completeness**: Includes error handling, edge cases, and tests

---

## Case Studies

### Case Study 1: Snowflake Data Warehouse Implementation

**Context**: Implementing data infrastructure with Claude Code assistance.

**Task**: Generate Snowflake DDL (Data Definition Language) for data warehouse.

**Result:**
- **First deployment success**: Generated DDL **passes all validation checks without errors**
- **Quality**: Production-ready on first attempt
- **Time savings**: Eliminates typical iteration cycles

**Implication**: Claude Code can generate complex database schema definitions reliably for immediate deployment.

### Case Study 2: Cortex Analyst Semantic Model

**Context**: Building semantic model for Cortex Analyst.

**Task**: Create semantic layer for business intelligence.

**Result:**
- **Iteration efficiency**: Succeeded in **exactly two iterations**
- **Accuracy**: Minimal refinement needed
- **Deployment ready**: Quick path to production

**Comparison**: Traditional approach typically requires many iterations to get semantic models right.

**Key Insight**: Claude Code understands complex data modeling requirements and produces accurate results with minimal iteration.

### Case Study 3: Medium Article Analysis Pipeline

**Project**: Analyzing 2,486 Medium articles with Claude Code.

**Pipeline:**
1. Data collection from Medium
2. Text processing and cleaning
3. Exploratory data analysis
4. Interactive visualization generation
5. Insight extraction

**Outcome:**
- **End-to-end automation**: Complete pipeline from raw data to insights
- **Interactive dashboards**: Generated visualizations ready for sharing
- **Comprehensive analysis**: Statistical analysis and pattern detection

**Key Insight**: Claude Code handles complete data science workflows, not just isolated tasks.

### Case Study 4: SQL Query Generation for Business Users

**Challenge**: Business analysts need data but lack SQL expertise.

**Implementation**: Natural language to SQL translation.

**Workflow:**
1. Business user asks question in plain English
2. Claude translates to SQL with explanation
3. Query reviewed and executed
4. Results delivered with interpretation

**Benefits:**
- **Democratization**: Non-technical users access data independently
- **Accuracy**: Correct queries from business questions
- **Learning**: Explanations help users understand SQL
- **Efficiency**: Faster insights without waiting for data team

**Key Insight**: Claude bridges gap between business questions and technical execution.

---

## Implementation Guidance

### Getting Started Checklist

**Environment Setup:**
- [ ] Choose Claude access method (API, Claude Code CLI, platform integration)
- [ ] Set up development environment (Jupyter, VSCode, etc.)
- [ ] Configure data access and credentials (securely)
- [ ] Create project structure and CLAUDE.md
- [ ] Establish version control (git)

**Data Preparation:**
- [ ] Identify data sources and access requirements
- [ ] Establish data security and privacy protocols
- [ ] Create sample or synthetic data for testing
- [ ] Document data schemas and business logic
- [ ] Set up data storage and processing infrastructure

**Workflow Development:**
- [ ] Develop prompt templates for common tasks
- [ ] Create code review and testing processes
- [ ] Establish documentation standards
- [ ] Define quality metrics and benchmarks
- [ ] Plan for model/code deployment

**Team Enablement:**
- [ ] Train team on effective prompting for data science
- [ ] Share best practices and prompt libraries
- [ ] Create guidelines for code review of AI-generated code
- [ ] Establish collaboration workflows
- [ ] Monitor usage and gather feedback

### Effective Prompting Best Practices

**Provide Comprehensive Context:**
- **Data description**: Format, size, columns, business meaning
- **Domain knowledge**: Industry context, business logic
- **Constraints**: Performance requirements, resource limits
- **Environment**: Libraries, versions, deployment target
- **Goals**: What insights or outputs are needed

**Specify Technical Details:**
- **Language and version**: Python 3.9, R 4.x, etc.
- **Libraries**: Specific packages and versions if important
- **Coding style**: PEP 8, specific conventions
- **Output format**: Script, notebook, function, class
- **Performance needs**: Speed, memory, scalability requirements

**Reference Project Files:**
- **Use @filename**: Reference CLAUDE.md, data dictionaries, existing code
- **Provide examples**: Show existing code for consistency
- **Specify conventions**: Naming, structure, documentation style

**Request Explanations:**
- **Reasoning**: Ask for explanation of approach
- **Trade-offs**: Request discussion of alternatives
- **Assumptions**: Make explicit any assumptions in code
- **Limitations**: Identify edge cases or limitations
- **Best practices**: Request adherence to industry standards

**Iterate Strategically:**
- **Start broad**: Initial exploration and understanding
- **Refine iteratively**: Incorporate findings into next prompts
- **Use todo lists**: Break complex tasks into steps
- **Save effective prompts**: Build personal prompt library
- **Learn patterns**: Identify what works for your domain

### Quality Assurance Framework

**Code Review Checklist:**
- [ ] **Functionality**: Does code do what's intended?
- [ ] **Correctness**: Are algorithms and logic sound?
- [ ] **Efficiency**: Are there performance bottlenecks?
- [ ] **Readability**: Is code clear and well-documented?
- [ ] **Error handling**: Are edge cases and errors handled?
- [ ] **Testing**: Are there tests? Do they cover key scenarios?
- [ ] **Security**: Any SQL injection, data leakage, or vulnerabilities?
- [ ] **Dependencies**: Are libraries appropriate and secure?

**Testing Strategy:**
- **Unit tests**: Test individual functions and modules
- **Integration tests**: Test component interactions
- **Data validation**: Verify outputs with known results
- **Edge cases**: Test boundary conditions and unusual inputs
- **Performance tests**: Benchmark speed and memory usage

**Documentation Standards:**
- **Code comments**: Explain complex logic and decisions
- **Docstrings**: Comprehensive function/class documentation
- **README**: Project overview and usage instructions
- **CHANGELOG**: Track versions and changes
- **Data documentation**: Schema descriptions and business logic

### Measuring Success

**Productivity Metrics:**
- Lines of code generated per hour/day
- Time to complete standard data science tasks
- Reduction in debugging time
- Faster iteration and experimentation

**Quality Metrics:**
- Code reliability (test pass rates)
- Bug rates in AI-generated code
- Code review feedback and revision rates
- Production deployment success rates

**Business Impact:**
- Faster insights and decision-making
- More experiments and models tested
- Improved model performance (more time for tuning)
- Cost savings from efficiency gains

**Team Metrics:**
- Developer satisfaction and experience
- Onboarding time for new team members
- Knowledge sharing and documentation quality
- Innovation rate (new techniques tried)

---

## Key Insights & Recommendations

### What Works Exceptionally Well

**Strengths:**
1. **Code generation**: Production-ready code in first attempt (many scenarios)
2. **Debugging**: Dramatically more efficient than trial-and-error
3. **SQL translation**: Accurate natural language to SQL
4. **Data manipulation**: Excellent with pandas, numpy operations
5. **Comprehensive solutions**: Complete pipelines, not just snippets
6. **Multiple languages**: Python, R, SQL support
7. **Documentation**: Generates clear explanations and comments

**Ideal Use Cases:**
- Data loading and preprocessing pipelines
- Exploratory data analysis automation
- SQL query generation and optimization
- Code debugging and refactoring
- Visualization creation
- Statistical modeling workflows
- Data pipeline development
- Documentation generation

### What Requires Validation

**Always Verify:**
1. **SQL queries**: Check for injection vulnerabilities, correctness
2. **Statistical methods**: Ensure appropriate for data and assumptions
3. **Performance**: Test with realistic data volumes
4. **Edge cases**: Validate handling of unusual inputs
5. **Dependencies**: Security check on recommended packages
6. **Business logic**: Confirm alignment with domain requirements

**Best Practices:**
- Never deploy AI-generated code without testing
- Review complex algorithms carefully
- Validate statistical assumptions
- Check for data leakage in ML pipelines
- Ensure reproducibility (seeds, versions)

### Future Opportunities

**Emerging Applications:**
1. **Real-time model monitoring**: Automated drift detection and alerting
2. **AutoML integration**: Enhanced automatic model selection and tuning
3. **Data quality automation**: Continuous data validation and cleaning
4. **Interactive dashboards**: More sophisticated visualization generation
5. **MLOps automation**: Complete ML lifecycle management

**Required Development:**
1. **Deeper library integration**: Direct interaction with data science tools
2. **Real-time data handling**: Streaming data analysis
3. **Domain-specific models**: Fine-tuning for specific industries
4. **Enhanced debugging**: Better error diagnosis and fixing
5. **Collaborative features**: Multi-user data science workflows

---

## Additional Resources

### Tools & Platforms
- **Claude Code CLI**: Terminal-based data science assistance
- **Jupyter integration**: Claude for notebook workflows
- **IDE plugins**: VSCode, PyCharm integration options
- **Data platforms**: Integration with Snowflake, Databricks, etc.

### Learning Resources
- **Effective prompting**: Data science-specific prompt engineering
- **Code quality**: Best practices for Python, R, SQL
- **Statistical methods**: When to use which technique
- **ML pipeline design**: Production ML system architecture

### Libraries & Frameworks
- **Data manipulation**: pandas, numpy, polars
- **Visualization**: matplotlib, seaborn, plotly, altair
- **ML/modeling**: scikit-learn, xgboost, lightgbm
- **Deep learning**: PyTorch, TensorFlow (with appropriate prompting)
- **Statistical**: statsmodels, scipy

### Documentation
- **Python Data Science Handbook**: Comprehensive reference
- **SQL Style Guide**: Best practices for query writing
- **ML Engineering**: Production ML system design
- **Clean Code**: Code quality principles

---

*This document represents current best practices as of 2025. Data science AI capabilities evolve rapidly. Always validate AI-generated code and analyses, maintain statistical rigor, and apply professional judgment. Use AI to accelerate development while ensuring correctness, security, and reproducibility.*
