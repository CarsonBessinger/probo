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
        St_array = np.zeros(int(engine.time_steps + 1))
        St_array[0] = spot
         
            
      # Random Draws (Reset Each j)
        epsilon = np.zeros(int(engine.time_steps + 1))
        epsilon = np.random.normal(size = int(engine.time_steps + 1))
        epsilon[0] = 0

        for k in range(1, int(engine.time_steps + 1)):
            St_array[k] = St_array[k-1] * np.exp(nudt[k] + sigsdt[k] * epsilon[k])
    # Arithmetic Average
        A = np.mean(St_array)

# Pass to Vanilla Payoff  
        CT = option.payoff(A) 
        sum_CT = sum_CT + CT
        sum_CT2 = sum_CT2 + CT*CT
    
    price = (sum_CT / engine.replications) * np.exp(-rate * expiry)
# SD and SE Not Currently being used    
    SD = np.sqrt((sum_CT2 - (sum_CT * (sum_CT / engine.replications))) * (np.exp(-2 * rate * expiry)) / (engine.replications - 1))
    SE = SD / np.sqrt(engine.replications)
    return (price,SE)