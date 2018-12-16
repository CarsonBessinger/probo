def NaiveAsianCall(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    dt = expiry / engine.time_steps
    
    nudt = np.zeros(int(engine.time_steps + 1))
    sigsdt = np.zeros(int(engine.time_steps + 1))
    
    for i in range(1, int(engine.time_steps + 1)):
        nudt[i] = (rate - dividend - 0.5 * volatility * volatility) * (dt)
        sigsdt[i] = volatility * np.sqrt(dt)

    sum_CT = 0
    sum_CT2 = 0

    for j in range(1, engine.replications + 1):
        ST = np.zeros(int(engine.time_steps + 1))
        ST[0] = spot
        productSt=1
        
        
        eps = np.zeros(int(engine.time_steps + 1))
        eps = np.random.normal(size = int(engine.time_steps + 1))
        eps[0] = 0
    
        for k in range(1, int(engine.time_steps + 1)):
            ST[k] = ST[k-1] * np.exp(nudt[k] + sigsdt[k] * eps[k])

        A = np.mean(ST)
        #G = gmean(ST)
        CT = option.payoff(A)
        sum_CT = sum_CT + CT
        sum_CT2 = sum_CT2 + CT*CT

    #portfolio_value = (sum_CT/engine.replications) * np.exp(-rate*expiry)
    SD = np.sqrt((sum_CT2 - (sum_CT * (sum_CT / engine.replications))) * (np.exp(-2 * rate * expiry)) / (engine.replications - 1))
    SE = SD / np.sqrt(engine.replications)
    price = (sum_CT / engine.replications) * np.exp(-rate * expiry)

    return(price,SE)
