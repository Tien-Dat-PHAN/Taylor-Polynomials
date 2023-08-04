import math
import numpy as np
import sympy as sp 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd


t, a = sp.symbols('t a')

print(t, a)

def taylor_terms(func, order, point, derivatives = None):
    '''
    find symbolic derivates and Talor terms
    func: symbolic function to approximate
    order: highest order derivative for Talor polynomial (int)
    point: point about which the function is approximated
    derivatives: list of symbolic derivatievs
    '''

    # initialize list of derivatives
    if derivatives is None:
        derivatives = [func.subs({t:a})]
    
    # check if highest order derivative is reached
    if len(derivatives) > order:
        #return list of talor terms evaluated using substitution
        return derivatives, [derivatives[i].subs({a: point}) / math.factorial(i) * (t - point) ** i for i in range(len(derivatives))]

    # differentiate function with respect to t
    derivative = func.diff(t)

    # append to list af sympolic derivative (substitude t with a)
    derivatives.append(derivative.subs({t:a}))

    # recursive call to find next term in Talor polynomial

    return taylor_terms(derivative, order, point, derivatives)

def taylor_polynomials(terms):
    '''
    find Taylor polynomials
    func: symbolic function to approximate
    order: highest order derivative for Taylor polynomial
    point: point about which the function is approximated
    derivatives: list of Taylor terms
    '''

    # initialize list
    polynomials = []

    # initialize taylor polynomial
    poly = None

    for term in range(len(terms)):
        # build up polynomial on each iteration
        poly = terms[term] if poly is None else poly + terms[term]

        polynomials.append(poly)

    return polynomials

def reg(x):
    if x == 1:
        return x
    
    return x*reg(x-1)
if __name__ == '__main__':

    # analysis label
    label = 'ln(t)'

    # symbolic function to approximate

    f = sp.log(t)

    #point about approximate
    approximation_point = np.pi

    # defune start, stop time
    start = 0.01
    stop = 2*sp.pi

    time = np.arange(start, stop, 0.1)

    # find talor polynomial term describing function f(t)
    symbolic_derivates, terms = taylor_terms(func=f,order= 4, point = approximation_point)
    polys = taylor_polynomials(terms)

    print(polys)
   
   # initialize plot
    fig, ax = plt.subplots()
    ax.set(xlabel = 't', ylabel ='y', title = 'Taylor Polynomial Approximation: {label}')
    legend = []

    for p, poly in enumerate(polys):
        ax.plot(time, [poly.subs({t: point}) for point in time])
        legend.append(f'P{p}')

    ax.plot(time, [f.subs({t: point}) for point in time])
    legend.append(f'f(t)')

    # create a data frame

    df = pd.DataFrame({'symbolic_derivates': symbolic_derivates,
                       'taylor_term': terms,
                       'polynomials': polys})
    
    # save and show the results

    ax.legend(legend)
    ax.grid()
    plt.savefig(f'taylor_{label}.png')
    plt.show()
    df.to_csv(f'taylor_{label}.csv', encoding ='utf-8')
    print(df.head(10))
