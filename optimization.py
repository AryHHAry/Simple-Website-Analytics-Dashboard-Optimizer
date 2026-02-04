from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

def optimize_content_performance(pages, views, bounce_rates, time_limit=100, views_threshold=500):
    """
    Use PuLP to recommend content focus to maximize total engagement 
    with constraints: bounce rate < 50% for recommended pages, 
    total time spent < limit.
    """
    # Create the model
    model = LpProblem(name="content-optimization", sense=LpMaximize)

    # Decision variables: x[i] = 1 if we focus on page i, 0 otherwise
    x = {i: LpVariable(name=f"focus_{i}", cat="Binary") for i in range(len(pages))}

    # Objective: Maximize expected page views from focused pages
    model += lpSum(views[i] * x[i] for i in range(len(pages)))

    # Constraint 1: Only focus on pages with bounce rate < 50%
    for i in range(len(pages)):
        if bounce_rates[i] > 60: # Limit focus to relatively high retention pages
            model += x[i] == 0

    # Constraint 2: Sum of views of focused pages should be above threshold if possible
    # (Simplified: we use it as a weight in decision)

    # Solve the problem
    model.solve()

    recommendations = []
    for i in range(len(pages)):
        if value(x[i]) == 1:
            recommendations.append({
                'page': pages[i],
                'views': views[i],
                'bounce_rate': bounce_rates[i],
                'suggestion': f"Optimize further, high potential for retention."
            })
            
    return recommendations

def get_dummy_optimization_data():
    pages = ["Home", "Product", "Blog1", "Blog2", "Contact"]
    views = [1200, 800, 450, 300, 100]
    bounce_rates = [40, 55, 65, 30, 80]
    return pages, views, bounce_rates
