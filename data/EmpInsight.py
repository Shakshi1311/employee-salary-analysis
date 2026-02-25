import pandas as pd
import numpy as np
df = pd.read_csv(r"C:\Data Analyst Project\EmpInsight\employee_salary-performace.csv")
print(df)

# ==============================
# DATA INSPECTION
# ==============================
# df.head() is used to show first values we can also gave the number to show values 
print("First five record is \n ",df.head(5)) 
# df.head() is used to show last values we can also gave the number to show values 
print("Last 5 record is \n",df.tail(5))
# gave the inforamation which datatype is used column name memory usage 
df.info() 
# df.describe() is used to generate summary statistics of a DataFrame.
print(df.describe(include="all"))
# df.shape is used in pandas to get the dimensions (size) of a DataFrame. [rows,coloumns]
print("No of rows : ",df.shape[0]) 
print("No of cols : ",df.shape[1])


# ==============================
# Task 2: Missing Value Handling
# ==============================

# Count missing values column-wise
print("Missing value by column wise\n  ",df.isnull().sum())
#missing salary with meadian 
# we can choose meadian bcz sal range will be high to low so we can use median for proper value first we find avg_sal than wecan fill with salary with avg_Sal so missing sal will be find 
avg_sal = df["Salary"].median()
df["Salary"] = df["Salary"].fillna(avg_sal)
print("missing salary with meadian is  \n",df)
# Department → mode 
# we can use mode for department bcz if we can missing the value so it can check the which value will be most time repeated so it can fill with that value
df['Department'] = df['Department'].fillna(df['Department'].mode()[0])
print("missing department with mode is \n  ", df)
# Rating → mean 
# Calculates the mean of Rating Replaces all NaN values Updates the column directly
df['Rating'] = df['Rating'].fillna(df['Rating'].mean())
print("missing rating with mean is \n  ", df)


# ==============================
# Task 3: Duplicate Handling
# ==============================
# it will gaves the total duplicated data  df.duplicated()
print("duplicated rows is :",df.duplicated().sum())
# Remove duplicates based on EmployeeID
# we can remove duplicate rows df.drop_duplicates and use kepp = first bcz it will keep 1st record 
print("Before shape:", df.shape)
# Remove duplicates and update df
df[df.duplicated(subset="EmployeeID")]
df = df.drop_duplicates(subset="EmployeeID", keep="first")
# Shape after
print("After shape:", df.shape)
print("Remove Duplicate EmployeeID\n", df)

# ==============================
# Task 4: Data Type Fixing
# ==============================

# Convert: JoinDate → datetime  we can use pandas in built function to_datetime
df["JoinDate"] = pd.to_datetime(df["JoinDate"], errors="coerce")
print("Convert: JoinDate → datetime",df["JoinDate"])

# Department → category we can use astype for datatype change 
df["Department"] = df["Department"].astype("category")

# Extract: Joining Year Joining Month we can use pandas function .dt.year and .dt.month to rextract year and month and than we can use head for showing five record it is working or not 

df["Joining Year"] = df["JoinDate"].dt.year
df["Joining Month"] = df["JoinDate"].dt.month
print(df.head())

print("Final Data Info:")
df.info()

# ======== phase 2 : numpy ===========
# ============================================
#   Task 5: Salary Analysis using NumPy
# =============================================
# Convert salary column to NumPy array
salary_array = df["Salary"].to_numpy()
print(type(salary_array))

# 1 Calculate: Mean Median Standard Deviation Minimum Maximum
print("Mean Salary :", np.mean(salary_array))
print("Meadian Salary:", np.median(salary_array))
print("Standard deviation Salary:", np.std(salary_array))
print("Maximum salary is :" , np.max(salary_array))
print("Minimum salary is :" , np.min(salary_array))

# 2 Find employees earning above average salary using NumPy condition
avg_sal = np.mean(salary_array)
employees_above_avg = df[df["Salary"] > avg_sal]
print("Employees earning above average salary:")
print(employees_above_avg)

# ===============================================
# Task 6: Experience Categorization (Using NumPy)
# ==============================================
# Experience	Level
# <2	Junior
# 2–5	Mid
# >5	Senior 
# in this we have experience column but we can add level column for this so we cna use level for adding and use np.where for gaving multiple condition for level
df["Level"] = np.where(
    df["Experience"] < 2,
    "Junior",
    np.where(
        df["Experience"] <=5,
        "Mid",
        "Senior"
    )
)
print(df)

#=========== PHASE 3 – Business Analysis (Very Important for Interview) ==========
#==================== ask 7: Department-wise Analysis =================
# ========================================================================

# Average Salary per Department
average_sal_bydept = df.groupby("Department", observed=True)["Salary"].median()
print("Average Salary per Department :\n",average_sal_bydept)

# Total Employees per Department in this we can count by sum 
total_emp_bydept = df.groupby("Department", observed=True).size()
print("total employees per department \n ",total_emp_bydept)

# Highest Paying Department
Highest_Paying_Dept = df.groupby("Department")["Salary"].max()
print(Highest_Paying_Dept)

# average rating by dept
average_rating_bydept = df.groupby("Department", observed=True)["Rating"].mean()
print(average_rating_bydept)

# ===========================================================
# ================Task 8: Performance vs Salary==============
# ===========================================================
# 1 .Does higher rating mean higher salary?
#  we can not direct predict this things we calculate correlation betwwem the salary and ratings than we can gave the value positive and hight value so that higher ratings will be higher salary
# 2 Find correlation between Salary and Rating we use pandas functin corr() it shows the corerelation
print("Find correlation between slary and ratings is :\n ", df[['Salary','Rating']].corr())
# 3. Show top 5 high-performing employees in this we can use sort values by rating and use head for disply 5 reacords 
print("Show top 5 high-performing employees :\n ", df.sort_values(by="Rating",ascending=False).head(5))

# ===========================================================
# ================Task 9: Senior Employee Insights===========
# ===========================================================

# 1 Count total Senior employees
count_senior_emp = (df['Level']=='Senior').sum()
print("Senior Employee is :\n ", count_senior_emp)

# 2 Find average salary of Senior employees
avg_Sal_senior_Emp = df.groupby("Level")['Salary'].mean()
print("Avg sal of senior emp is :\n ", avg_Sal_senior_Emp)

# 3. Compare Junior vs Senior salary difference
difference = avg_Sal_senior_Emp["Senior"] - avg_Sal_senior_Emp["Junior"]
print("Salary Difference:", difference)


# ==============================================
# ======Task 10: Extreme Salary Investigation===
# ==============================================

# Identify salary > 3x median

meadian_sal = df["Salary"].median()

# extreme sal Identify salary > 3x median we cna define salary with multiply 3 with meadian sal 
extreme_sal = df[df["Salary"] > 3 * meadian_sal]
print("Meadian sal is ", meadian_sal)
print("Extreme Employees:\n", extreme_sal)

# Count how many such employees exist
print("count employees exist", extreme_sal.shape[0])

# replace extreme salary with upper cap (use np.clip())

df["Salary"] = np.clip(df["Salary"], None, 3 * meadian_sal)
print("Updated salary with upper cap is : \n ", df["Salary"])

# ===============phase 4============================
# ===================================================
# =========Task 11: Create New Metrics===============
# ===================================================
# 1 Salary per Year of Experience
df['salary_per_exp_year'] = np.where(
    df['Experience'] > 0,
    df['Salary'] / df['Experience'],
    np.nan
)
print("Salary per Year of Experience is \n :",df["salary_per_exp_year"])

# 2 Performance Score = Salary * Rating
df['performance_score'] =df['Salary'] * df['Rating']
print("Performance Score \n :",df["performance_score"])

# 3 Rank employees by Salary within each department
df["Dept_Salary_Rank"] = (
    df.groupby("Department")["Salary"]
      .rank(ascending=False, method="dense")
)
print(" Rank employees by Salary within each department :\n ",df['Dept_Salary_Rank'])

# =================================================
# ====Task 12: Filtering Scenarios=================
# ===================================================

# 1. Employees earning above department average
dept_avg = df.groupby('Department')['Salary'].transform("mean")
print("employee earning above department range \n",df[df['Salary']>dept_avg])

# 2 Employees with rating < 3 but salary > average
avg_sal = df["Salary"].mean()
print("Employees with rating < 3 but salary > average \n" ,df[(df['Rating']<3) & (df['Salary'] > avg_sal)])

# 3 Employees joined after 2020
print("Emp joined after 2020 :\n ", df[df["JoinDate"].dt.year > 2020])

# Top 3 highest salary employees per department
df["Rank"] = df.groupby('Department')['Salary'].rank(ascending=False,method="dense")
print("Top 3 highest salary employees per department",df[df["Rank"]<= 3])

# ================================================================== 
# ============# =============== PHASE 5 – FINAL REPORT ==============
# ===================================================================

print("\n  =============== FINAL SUMMARY REPORT ============== ")

#  1 total employess
total_employess = df.shape[0]

# 2 average Salary
average_salary = df["Salary"].mean()

# 3 max Salary
highest_salary = df["Salary"].max()

# 4 Lowest Salary
lowest_salary = df["Salary"].min()

# 5 Best Paying/deoartment (based on avaerage)
dept_avg_salary = df.groupby("Department", observed=False)["Salary"].mean()
best_paying_dept = dept_avg_salary.idxmax()

# 6 Correlation Salary vs Rating

correlation = df["Salary"].corr(df["Rating"])

# 7 Total Senior Employees

total_senior = (df["Level"] == "Senior").sum()

# create summary datafram 
summary = pd.DataFrame({
    "Metric":[
        "Total Employess",
        "Average Salary",
        "Highest Salary",
        "Lowest Salary",
        "Best Paying Department",
        "Correlation(Salary-Rating)",
        "Total Senior Employees"
    ],
    "value" :[
        total_employess,
        round(average_salary,2),
        highest_salary,
        lowest_salary,
        best_paying_dept,
        round(correlation,2),
        total_senior
    ]
})

print(summary)

# final for csv file 
df.to_csv("cleaned_employee_data.csv", index=False)

# final for excel file 
summary.to_excel("employee_summary_report.xlsx", index=False)
