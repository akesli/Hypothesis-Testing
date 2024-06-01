import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import pingouin

#convert csv files to pandas data frame
women = pd.read_csv(r"C:\Users\akesli\Documents\GitHub\Data Camp Codes\Hypotesis Testing\women_results.csv")
men = pd.read_csv(r"C:\Users\akesli\Documents\GitHub\Data Camp Codes\Hypotesis Testing\men_results.csv")

#calcualte the total amountof goals in each game 
women['total_score'] = women['home_score'] + women['away_score']
men['total_score'] = men['home_score'] + men['away_score']

#filter results for FIFA World Cup games only and Convert data to datatime and filter for games after 2002-01-01
women['date'] = pd.to_datetime(women['date'])
men['date'] = pd.to_datetime(men['date'])
women_subset = women[(women['date'] > '2002-01-01') & (women['tournament'].isin(['FIFA World Cup']))]
women_subset['group'] = 'women'
men_subset = men[(men['date'] > '2002-01-01') & (men['tournament'].isin(['FIFA World Cup']))]
men_subset['group'] = 'men'
#check histograms
women_subset['total_score'].hist()
plt.show()
plt.clf()

men_subset['total_score'].hist()
plt.show()
plt.clf()

#not normally distributed use Wilcoxon-Mann-Whitney test
#combine the two data frames
both = pd.concat([women_subset, men_subset], axis=0, ignore_index=True)
both_subset = both[['total_score', 'group']]
both_subset_wide = both_subset.pivot(columns='group', values='total_score')
results = pingouin.mwu(x=both_subset_wide['women'], y=both_subset_wide['men'], alternative='greater')

#get p-value
p_val = results['p-val'].values[0]

#use significance value
if p_val <= 0.1:
    result = 'reject'
else:
    result = 'fail to reject'
    
result_dict = {"p_val": p_val, "result": result}
print(result_dict)
