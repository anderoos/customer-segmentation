# Segmenting Customers based on E-Commerce Customer Data
#### Andrew Cheng, Liam Odonovan, Gloria Gao, Jerry Yu
-----
![churn](https://raw.githubusercontent.com/anderoos/customer-segmentation/main/Images/readme_banner.png)

## Introduction
Link to presentation: [Google Slides](https://docs.google.com/presentation/d/1nCEqAgGCB1ZGswAT7L4pUVOp281T8ia1ymjsokjlIcI/edit#slide=id.p)

The phrase "The customer is always right!" by Harry Gordon Selfridge was coined over a century ago and is still relevant today. When operating a business, understanding your customer's behaviors and preferences is beneficial to many aspects of a business and is key to keeping a competitive edge. Understanding customer behaviors can improve business operations, improve marketing impact, and everything in between. Ultimately this can lead to a boost in sales, customer engagement and customer brand loyalty. Using ecommerce data retrived from [Kaggle](https://www.kaggle.com/datasets/shriyashjagtap/e-commerce-customer-for-behavior-analysis?select=ecommerce_customer_data_custom_ratios.csv), the goal of this project is to uncover trends in business performance, analyze customer behaviors and leverage machine learning to predict future customer behavior based on metrics like churn and calculated low-valued customers.

By understanding different customer segments and retention from their first purchases, we hope to use this insight to strategically allocate resources to drive customer engagement and build stronger relationships with our customer base. This can be accomplished in the form of personalized promotional offers, targetted/ geotargetted ad campaigns, and more.

## Data Review and Cleanup for Visualization
 - Categorize customers into age ranges.
 - Analyzing purchase behavior and categorizing customers into classes/types based on their purchase count.
 - Identifying popular product categories, age distribution, gender distribution, and return rate.

## Visualization and Findings
1. **Trend Forecast and Historical Monthly Trend by Category**
The trend forecast model shows an overall upward trajectory in purchasing behavior over time, with fluctuations within quarterly periods possibly influenced by seasonal trends, marketing campaigns, or economic conditions. Specifically, the Books category exhibits a moderately significant upward trend (P-value = 0.35) throughout the year, while the Clothing category remains relatively constant (P-value = 0.46). The Electronics category shows a moderately significant downward trend (P-value = 0.15), and the Home category displays a moderately significant upward trend (P-value = 0.36) from January to December.

2. **Purchase Differences by Age and Category**
Purchase differences by age and category reveal that older males (65+) dominate book purchases, while females generally spend slightly more across all age groups. Clothing purchases show slight variation by gender, with increased spending in older age groups. Electronics purchases indicate slightly lower spending by females, with higher expenditures in older age groups for both genders. Significant home category purchases occur among both genders aged 45-54, and females aged 35-44 show a notable increase in spending.

3. **Customer Loyalty vs Purchasing Power**
Bronze customers representing 51.33% of purchases, targeting efforts towards this group, particularly those in the 25-34 age range, could significantly enhance upselling opportunities, revenue, and customer loyalty.

4. **Return Rate & Category Breakdown**
The overall return rate across all categories is 6%. Clothing items have the highest return rate, while books have a slightly lower return rate than clothing items, but they remain relatively high. And electronics have the lowest return rate among the analyzed product categories.

## Approach
We first used EDA to explore our dataset to uncover unusual/ interesting behaviors in this dataset. This allows us to identify areas of concern before using advanced analytical tools. We then attemped to use unsupervised machine learning methods PCA and KMeans clustering with pairplots to segment our customer base based on their spending habits. Unforunately, PCA proved unfruitful and didn't demonstrate strong clusters/ segments in our dataset. We then pivoted and used RFM analysis (Recency, Frequency, Monetary) to segment our custoemrs, which often is referred to as the gold standard of customer segmentation. RFM analyzes customer purchasing patterns and scores them based on RFM metrics. Using these metrics and churn, we employed Random Forest Classification supervised learning model to predict low-valued customer segments and churn based on their first purchases.

## Conculsions and Limitations
When attempting to predict the low-value customer segement and churn, we were able to achieve 77% and 85% respectively. Although the accuracy of these predictions are not as high as we would like, these scores suggest there is a relationship between these metrics and their first purchase. More data is likely required to achieve higher accuracy scores.
