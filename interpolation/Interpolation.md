Interpolation
===

Index
---
<!-- TOC -->
- [Neville's Algo](#Neville's_Algo)
- [Error in Polynomial Interpolation](#Error-in-Polynomial-Interpolation)
- [Cubic Spline](#Cubic-Spline)
- [MLES](#MLES)
<!-- /TOC -->

## Neville's Algo

- ![nev_algo]
- Example:
    ![nev_plot](images/nev_plot.jpg)
- correctness:
    - for ![nev_algo1] holds
    - for other points,<br>
      ![nev_algo2]
    - uniqueness
    
[nev_algo]: http://chart.apis.google.com/chart?cht=tx&chl=P_{i_0,i_1,\dots,i_k}(x)=\frac{(x-x_{i_0})P_{i_1,\dots,i_k}(x)-(x-x_{i_k})P_{i_0,\dots,i_{k-1}}(x)}{x_{i_k}-x_{i_0}}
[nev_algo1]: http://chart.apis.google.com/chart?cht=tx&chl=i_0,i_k
[nev_algo2]: http://chart.apis.google.com/chart?cht=tx&chl=j=i_1,\dots,i_{k-1}

## How good is Polynomial Interpolation?

![I_form](images/poly1.jpg)

- if ![poly_1] is one of ![poly_2], holds
- else, consider ![poly_3] <br>
for k that makes ![poly_4] <br>
hence ![poly_5] <br>
- Then we have n+1 zeros
- F' has at least n+1 zeros in **I**, F'' has at least n zeros ,...
- ![poly_6] has at least 1 zero in **I** (![poly_8])
- ![poly_7]
- ...

> [Reference STBU 2.1.4](#How_good_is_Polynomial_Interpolation)

[poly_1]: http://chart.apis.google.com/chart?cht=tx&chl=\bar{x}
[poly_2]: http://chart.apis.google.com/chart?cht=tx&chl=x_j
[poly_3]: http://chart.apis.google.com/chart?cht=tx&chl=F(x)=f(x)-P_{01...n}(x)-kw(x)
[poly_4]: http://chart.apis.google.com/chart?cht=tx&chl=F(\bar{x})=f(\bar{x})-P_{01...n}(\bar{x})-kw(\bar{x})
[poly_5]: http://chart.apis.google.com/chart?cht=tx&chl=k=\frac{f(\bar{x})-P(\bar{x})}{w(\bar{x})}
[poly_6]: http://chart.apis.google.com/chart?cht=tx&chl=F^{n%2B1}
[poly_7]: http://chart.apis.google.com/chart?cht=tx&chl=k=\frac{f^{n+1}(\xi)}{(n%2B1)!}
[poly_8]: http://chart.apis.google.com/chart?cht=tx&chl=\xi

## Cubic Spline

### Exists?

![f_c1]

Given ![f_c8], 4n unkonwn

- ![f_c2]<br>
- ![f_c3]<br>
- ![f_c4]<br>
- ![f_c5]<br>

[f_c1]:http://chart.apis.google.com/chart?cht=tx&chl=P_i(x)=a_ix^3%2Bb_ix^2%2Bc_ix%2Bd_i
[f_c2]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}(x_{i-1})=y_{i-1}
[f_c3]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}(x_{i})=y_{i}
[f_c4]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}'(x_{i})=P_i'(x_{i})
[f_c5]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}''(x_{i})=P_i''(x_{i})
[f_c8]:http://chart.apis.google.com/chart?cht=tx&chl=(x_0,y_0),(x_1,y_1),\dots,(x_n,y_n)

We have n, n, n-1, n-1, in all 4n-2 equations with 2 degrees freedom

Common constraints:

- A. Natural Spline:<br>
![f_c6]<br>
- B. Periodic:<br>
![f_c7]<br>
for k = 0, 1, 2
- C. First Derivative Assignment:<br>
![f_c9]<br>
![f_c10]<br>

[f_c6]:http://chart.apis.google.com/chart?cht=tx&chl=S''_{\Delta}(a)=S''_{\Delta}(b)=0
[f_c7]:http://chart.apis.google.com/chart?cht=tx&chl=S^{k}_{\Delta}(a)=S^{k}_(b)
[f_c9]:http://chart.apis.google.com/chart?cht=tx&chl=S'_{\Delta}(a)=y_0'
[f_c10]:http://chart.apis.google.com/chart?cht=tx&chl=S'_{\Delta}(b)=y_n'

### Why Cubic?

- **Thm:**<br> 
Let ![w_1]<br>
suppose f is sufficiently nice (see STBU), then<br>
![w_2]<br>
**I** = ![I_form](images/I_form.jpg)

[w_1]:http://chart.apis.google.com/chart?cht=tx&chl={||f||}^2=\int_{a}^{b}{||f''(x)||}^2dx
[w_2]:http://chart.apis.google.com/chart?cht=tx&chl={||f-S_{\Delta}||}^2={{||f||}^2-{||S_{\Delta}||}^2-2I}

> [Reference STBU 2.4.1.4](#Cubic_Spline)

- **Thm:**<br>
A or B or C constraint above holds, ![w_4]<br>
Minimum Curvature Property <br>
![I_form2](images/I_form2.jpg)
![w_5]

[w_3]:http://chart.apis.google.com/chart?cht=tx&chl={||f||}^2=\int_{a}^{b}{||f''(x)||}^2dx
[w_4]:http://chart.apis.google.com/chart?cht=tx&chl=I=0
[w_5]:http://chart.apis.google.com/chart?cht=tx&chl=f(x_i)=S_{\Delta}(x_i)

> [Reference STBU 2.4.1.5](#Cubic_Spline) 

- **Calculation**

    - ![cubic_c1]
    - ![cubic_c2]
    - ![cubic_c3]
    - ![cubic_c4]
    - ![cubic_c5]
    - ![cubic_c6]
    - ![cubic_c7]
    - ![cubic_c8]
    - after that, 4n equations are reduced to n+1 unkowns, ![cubic_c9]
        - ![cubic_c10]
        - ![cubic_c11]
        - n - 1 equations
    
    - we have: 
        - ![cubic](images/cubic.jpg)
    - ![cubic](images/cubic3.jpg)
    - If we have natural spline, we have:
        - ![cubic_c12]

[cubic_c1]:http://chart.apis.google.com/chart?cht=tx&chl=S(x)=P_i(x),\\,\\,x\in[x_{i-1},\\,x_i]\\,,i=1,2,\dots,n
[cubic_c2]:http://chart.apis.google.com/chart?cht=tx&chl=P_i(x)=a_i(x-x_{i-1})^3%2Bb_i(x-x_{i-1})^2%2Bc_i(x-x_{i-1})%2Bd_i
[cubic_c3]:http://chart.apis.google.com/chart?cht=tx&chl=m_i=S''(x_i),\\,i=1,2,\dots,n
[cubic_c4]:http://chart.apis.google.com/chart?cht=tx&chl=P_i(x)=y_{i-1}\\,\right\\,d_i=y_{i-1}
[cubic_c5]:http://chart.apis.google.com/chart?cht=tx&chl=m_{i-1}=S''(x_{i-1})=P''_{i-1}(x_{i-1})=6a_i(x_{i-1}-x_{i-1})%2B2b_i
[cubic_c6]:http://chart.apis.google.com/chart?cht=tx&chl=b_i=\frac{m_{i-1}}{2}
[cubic_c7]:http://chart.apis.google.com/chart?cht=tx&chl=P''_i(x_i)=P''_{i%2B1}(x_i)\\,\right\\,a_i=\frac{m_i-m_{i-1}}{6h_i},\\,h_i=x_{i}-x_{i-1}
[cubic_c8]:http://chart.apis.google.com/chart?cht=tx&chl=P_i(x)=y_i,\\,c_i=\frac{y_i-y_{i-1}}{h_i}-\frac{m_{i-1}%2B2m_{i-1}}{6}
[cubic_c9]:http://chart.apis.google.com/chart?cht=tx&chl=m_i,\\,i=0,1,\dots,n
[cubic_c10]:http://chart.apis.google.com/chart?cht=tx&chl=P'_i(x)=P'_{i%2B1}(x),\\,\right\\,\mu_i=\frac{h_i}{h_i%2Bh_{i%2B1}}\\\\\lambda_i=\frac{h_{i%2B1}}{h_i%2Bh_{i%2B1}}
[cubic_c11]:http://chart.apis.google.com/chart?cht=tx&chl=\frac{6}{h_i%2Bh_{i+1}}(\frac{y_{i+1}-y_i}{h_{i%2B1}}-\frac{y_i-y_{i-1}}{h_i})=d_i
[cubic_c12]:http://chart.apis.google.com/chart?cht=tx&chl=S''(x_0)=S''(x_n)=0,\\\\\lambda_0=0,\\,d_0=0,\\\\\mu_n=0,d_n=0.

- Why non-singular?

    - proof 1:<br>
      [reference STBU](#Cubic_Spline)
    
    - proof 2:
        - For ![inv_1]<br>
        ![inv_2]<br>
        we have:<br>
        ![cubic](images/cubic.jpg)
        ![inv_3]<br>
        ![inv_4]
        - let C=A-2I, <br>
        C = ![cubic](images/cubic2.jpg)
        ![inv_5]
        - propostion: ![inv_6]
        - suppose A is not non-singular, we have ![inv_7]
        - ![inv_8]
        

[inv_1]:http://chart.apis.google.com/chart?cht=tx&chl=P_{N*N}=(P_{ij})
[inv_2]:http://chart.apis.google.com/chart?cht=tx&chl=\\,\varphi(P)=\underset{i}{max}(\sum_{k=1}^{n}|P_{ik}|)\\,
[inv_3]:http://chart.apis.google.com/chart?cht=tx&chl=\mu_n=1\\,or\\,0\\,,\lambda_0=1\\,or\\,0\\\\\lambda_i,\mu_i>0,\\,\lambda_i%2B\mu_i=1,\\,j=1,\dots,n-1
[inv_4]:http://chart.apis.google.com/chart?cht=tx&chl=\lambda_j=\frac{h_{j%2B1}}{h_j%2Bh_{j%2B1}},\\,\mu_j=1-\lambda_j
[inv_5]:http://chart.apis.google.com/chart?cht=tx&chl=\varphi(C)=1
[inv_6]:http://chart.apis.google.com/chart?cht=tx&chl=\varphi(PQ){\leq}\varphi(P)\varphi(Q)
[inv_7]:http://chart.apis.google.com/chart?cht=tx&chl=A\vec{X}=\vec{0}
[inv_8]:http://chart.apis.google.com/chart?cht=tx&chl=\varphi(C)\varphi(X)\geq\varphi(CX)=\varphi(\(A-2I\)X)=2\varphi(X)

## MLES

> [Reference More Yield Curve Modelling at the Bank of Canada page 41- 48](#Cubic_Spline)

### discount factor & long term instantaneous forward rate

- discount factor:<br>
![mle1]<br>
- Note d(0) = 1  -> ![mle2]<br>
- ![zeta] are constants, D is dimension<br>

- argue ![alpha] is constant (long term instantaneous forward rate?)
    - try with ![mle3]<br>
    
    - ![mle4]<br>
    ![mle5]<br>
    but we have ![mle10]
    
    - ![mle2] -> at least one ![onezeta]<br>
    take ![mle6] as the smallest index s.t. ![mle7]<br>
    - ![mle8]<br>

[mle2]:http://chart.apis.google.com/chart?cht=tx&chl=\zeta_{1}%2B\zeta_{2}%2B\dots%2B\zeta_{D}=1
[mle1]:http://chart.apis.google.com/chart?cht=tx&chl=d(t)=\sum_{k=1}^{D}\zeta_{k}e^{-k{\alpha}t}
[alpha]:http://chart.apis.google.com/chart?cht=tx&chl=\alpha
[zeta]:http://chart.apis.google.com/chart?cht=tx&chl=\zeta_{1},\zeta_{2},\dots,\zeta_{k}
[mle3]:http://chart.apis.google.com/chart?cht=tx&chl=\lim_{t\to\infty}\frac{d(t)}{\zeta_{1}e^{-{\alpha}t}}?=1
[mle4]:http://chart.apis.google.com/chart?cht=tx&chl=d_1(t)=e^{-2%t},\zeta_{1}=1,\alpha=2%
[mle5]:http://chart.apis.google.com/chart?cht=tx&chl=d_2(t)=0%2Be^{-2\time1%t},\zeta_{1}=0,\zeta_{2}=1,\alpha=1%
[onezeta]:http://chart.apis.google.com/chart?cht=tx&chl=\zeta_{i}\ne0
[mle6]:http://chart.apis.google.com/chart?cht=tx&chl=i_0
[mle7]:http://chart.apis.google.com/chart?cht=tx&chl=\zeta_{i_0}\ne0
[mle8]:http://chart.apis.google.com/chart?cht=tx&chl=\lim_{t\to\infty}\frac{d(t)}{\zeta_{i_0}e^{-{\alpha}t}}=1
[mle9]:http://chart.apis.google.com/chart?cht=tx&chl=i_0\alpha
[mle10]:http://chart.apis.google.com/chart?cht=tx&chl=d_{1}(t)=d_{2}(t)

- ![mle9] is instantaneous forward rate <br>

    - ![ins_1]
    > [reference JOHN HULL](#MLE)
    
    - ![ins_2]<br>
    ![ins_3]<br>
    ![ins_4]<br>
    
    - ![ins_5]<br>
    ![ins_7]<br>
    Then we can prove ![ins_6]
    
    
    
[ins_1]:http://chart.apis.google.com/chart?cht=tx&chl=f_t=R_t%2Bt\frac{{\pa}R_t}{{\pa}t}
[ins_2]:http://chart.apis.google.com/chart?cht=tx&chl=d(t)=e^{-R_t{\time}t}
[ins_3]:http://chart.apis.google.com/chart?cht=tx&chl=R_t=-\frac{1}{t}\ln{d(t)}
[ins_4]:http://chart.apis.google.com/chart?cht=tx&chl=\frac{{\pa}R}{{\pa}t}=\frac{1}{t^2}\ln{d(t)}-\frac{d'(t)}{td(t)}
[ins_5]:http://chart.apis.google.com/chart?cht=tx&chl=f_t=-\frac{d'(t)}{d(t)}
[ins_6]:http://chart.apis.google.com/chart?cht=tx&chl=\lim_{t\to\infty}f_t=i_o\alpha
[ins_7]:http://chart.apis.google.com/chart?cht=tx&chl=\lim_{t\to\infty}f_t=\frac{i_0\alpha\zeta_{i_0}e^{-i_0{\alpha}t}%2B\dots}{\zeta_{i_0}e^{-i_0{\alpha}t}%2B\dots}

### Calibration using Bond Price

- ![cab_1]<br>
![m_i] is the number of cash flows of bond i,
![c_ij] is the magnitude of cash flow at ![tau_ij]

[cab_1]:http://chart.apis.google.com/chart?cht=tx&chl=\hat{P}=\sum_{j=1}^{m_i}c_{ij}d(\tau_{ij})
[m_i]:http://chart.apis.google.com/chart?cht=tx&chl=m_i
[tau_ij]:http://chart.apis.google.com/chart?cht=tx&chl=\tau_{ij}
[c_ij]:http://chart.apis.google.com/chart?cht=tx&chl=c_{ij}

- ![cab_2]

[cab_2]:http://chart.apis.google.com/chart?cht=tx&chl=\vec{Z}=(\zeta_{1},\dots,\zeta_{D})

- ![cab_3]<br>
![cab_4]<br>
![cab_5]<br>
where ![cab_6]

[cab_3]:http://chart.apis.google.com/chart?cht=tx&chl=\hat{P_i}=\sum_{j=1}^{m_i}c_{ij}\sum_{k=1}^{D}\zeta_{k}e^{-k{\alpha}\tau_{ij}}
[cab_4]:http://chart.apis.google.com/chart?cht=tx&chl==\sum_{k=1}^{D}\sum_{j=1}^{m_i}c_{ij}e^{-k{\alpha}\tau_{ij}}\zeta_{k}
[cab_5]:http://chart.apis.google.com/chart?cht=tx&chl==\sum_{k=1}^{D}H_{ik}\zeta_{k}
[cab_6]:http://chart.apis.google.com/chart?cht=tx&chl=H_{ik}=\sum_{j=1}^{m_i}c_{ij}e^{-k{\alpha}\tau_{ij}

- with N bonds ![cab_7]
- ![HZP](images/HZP.jpg)
- ![cab_8]

[cab_7]:http://chart.apis.google.com/chart?cht=tx&chl=\vec{P}=(P_1,P_2,\dots,P_N)
[cab_8]:http://chart.apis.google.com/chart?cht=tx&chl=\vec{P}=H\vec{Z}

- **Three Situations:**

    - <b>If N = D: </b><br>
    ![mle2], actually D-1 Bonds<br>
    if H is invertible, ![cab_9] (exercise, when is H a good one?)<br>
    
    - <b> If N < D </b> decrease D <br>
    - <b> If N > D </b> <br>
    Minimize ![cab_10]
    
[cab_9]:http://chart.apis.google.com/chart?cht=tx&chl=\vec{Z}=H^{-1}\vec{P}
[cab_10]:http://chart.apis.google.com/chart?cht=tx&chl=L(\vec{Z})=\sum_{i=1}^{N}w_i{(\hat{P_i}-P_i)}^2

- Paper suggests ![cab_11] is the reciprocal of the modified duration of the ith bond

    - ![W](images/W.jpg)
    - ![cab_12]
    - ![cab_13]
    - ![cab_14] for a = 1, ..., D
    - ![cab_15]<br>
    since ![cab_16]
    - if invertible, ![cab_17]

- Why reciprocal of modified duration? Price, Yield, more discrepancy at the end

[cab_11]:http://chart.apis.google.com/chart?cht=tx&chl=w_i
[cab_12]:http://chart.apis.google.com/chart?cht=tx&chl=\frac{{\pa}L(\vec{Z})}{{\pa}\zeta_{a}}=\sum_{i=1}^{N}w_i2(\hat{P_i}-P_i)\frac{{\pa}\hat{P}}{{\pa}\zeta_a}
[cab_13]:http://chart.apis.google.com/chart?cht=tx&chl=\frac{{\pa}\hat{P}}{{\pa}\zeta_a}=\sum_{j=1}^{m_i}C_{ij}e^{-a{\alpha}\tau_{ij}}=H_{ia}
[cab_14]:http://chart.apis.google.com/chart?cht=tx&chl=\frac{{\pa}L(\vec{Z})}{{\pa}\zeta_{a}}=\sum_{i=1}^{N}2W_i(\hat{P_i}-P_i)H_{ia}}=0
[cab_15]:http://chart.apis.google.com/chart?cht=tx&chl=H^TW(\vec{\hat{P}}-\vec{P})=\vec{0}
[cab_16]:http://chart.apis.google.com/chart?cht=tx&chl=\vec{\hat{P}}=H\vec{Z},H^TWH\vec{Z}=H^TW\vec{P}
[cab_17]:http://chart.apis.google.com/chart?cht=tx&chl=\vec{Z}={(H^TWH)}^{-1}H^TW\vec{P}