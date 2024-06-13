import math

# INSURANCE PRICING WEIGHTINGS/COSTS
# This is the base premium cost of the pension scheme based on the employee's salary, tenure and contribution percentage
TOTAL_PENSION_BASE_FACTOR = 0.03
# Males have typically shorter lifes, so a slight discount is applied
MALE_FACTOR = -0.08
# The reverse applies to females
FEMALE_FACTOR = 0.07
# Smokers have a shorter lifespan, so a discount is applied
SMOKING_FACTOR = -0.15
# Family people tend to live longer, so a slight increase is applied
FAMILY_FACTOR = 0.05
DISABILITY_FACTOR = 0.05 
# The cost factor of pension parts that will be provided to either a partner or children
PENSION_AFTER_DEATH = 0.025

MALE_LIFE_EXPECTANCY = 78
FEMALE_LIFE_EXPECTANCY = 82

def calc_pension_years(employee:dict, pension_params:dict):
    years_till_pension = max(pension_params['years_left'], 0)
    max_life_expectancy = MALE_LIFE_EXPECTANCY if employee['gender'] == 'Male' else FEMALE_LIFE_EXPECTANCY
    pension_years = max_life_expectancy - employee['age'] - years_till_pension 
    return pension_years

def estimate_pension_cost(employee: dict, pension_params: dict):
    # This naively assumes that a given employee will have had the salary for the entire tenure
    total_pension = employee['salary'] * employee['tenure'] * employee['contrib_percentage']
    pension_years = calc_pension_years(employee, pension_params)
    # The assumption is made that inflation increases will only be applied once an employee is a pensioner
    # The inflation increases are provided over the final pension amount at the first day of retirement
    inflation_adjusted_pension = total_pension * pow(1 + (pension_params['inflationary_increase'] / 100), pension_years)
    cost = inflation_adjusted_pension * TOTAL_PENSION_BASE_FACTOR
    if employee['gender'] == 'Male':
        cost += cost * MALE_FACTOR
    elif employee['gender'] == 'Female':
        cost += cost * FEMALE_FACTOR
    if employee['smoking']:
        cost += cost * SMOKING_FACTOR
    if employee['married'] or employee['dependents']:
        cost += cost * FAMILY_FACTOR
    cost += pension_params['disability_increase'] * DISABILITY_FACTOR
    cost += pension_params['pension_percentage_after_death'] * PENSION_AFTER_DEATH
    # print("Cost for employee: ", employee['id'], " is: ", cost, " with pension years: ", pension_years, " and inflation adjusted pension: ", inflation_adjusted_pension)
    return cost


def estimate_pensions_cost(employees: list[dict], pensions_params: list[dict]):
    total_cost = 0
    for employee, pension_params in zip(employees, pensions_params):
        # print(employee, pension_params)
        total_cost += estimate_pension_cost(employee, pension_params)
    return total_cost

def calc_avg_pension_length(employees: list[dict], pensions_params: list[dict]):
    total_years = 0
    for employee, pension_params in zip(employees, pensions_params):
         total_years += calc_pension_years(employee, pension_params)
    return math.ceil(total_years / len(employees))

def get_insurance_premium_cost(employees_data: list[dict], employees_pensions_params: list[dict]):
    # Cost of premium that will cover the pensions of all employees for their lifetimes
    total_premium_cost = estimate_pensions_cost(employees_data, employees_pensions_params)
    yearly_premium = total_premium_cost / calc_avg_pension_length(employees_data, employees_pensions_params)
    return [total_premium_cost, yearly_premium]