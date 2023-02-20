import numpy as np
def split_step_schrodinger(psi_0, dx, dt, V, N, x_0 = 0., k_0 = None, m = 1.0, non_linear = False):

    len_x = psi_0.shape[0]

    x = x_0 + dx*np.arange(len_x)

    dk_x = (2*np.pi)/(len_x*dx)
    if k_0 == None:
        k_0 = -np.pi/dx
    k_x = k_0+dk_x*np.arange(len_x)

    psi_x = np.zeros((len_x,N), dtype = np.complex128)
    psi_k = np.zeros((len_x,N), dtype = np.complex128)
    psi_mod_x = np.zeros((len_x), dtype = np.complex128)
    psi_mod_k = np.zeros((len_x), dtype = np.complex128)
    psi_x[:,0] = psi_0

    if not non_linear:
        V_n = V(x)
    else:
        V_n = V(x,psi_0)

    def _compute_psi_mod(j):
        return (dx/np.sqrt(2*np.pi))*psi_x[:,j]*np.exp(-1.0j*k_x[0]*x)

    def _compute_psi(j):
        psi_x[:,j] = (np.sqrt(2*np.pi)/dx)*psi_mod_x*np.exp(1.0j*k_x[0]*x)
        psi_k[:,j] = psi_mod_k*np.exp(-1.0j*x[0]*dk_x*np.arange(len_x))

    def _x_half_step(j,ft = True):
        if ft == True:
            psi_mod_x[:] = np.fft.ifft(psi_mod_k[:])
        if non_linear:
            V_n[:] = V(x,psi_x[:,j])
        psi_mod_x[:] = psi_mod_x[:]*np.exp(-1.0j*(dt/2.)*V_n)   

    def _k_full_step():
        psi_mod_k[:] = np.fft.fft(psi_mod_x[:])
        psi_mod_k[:] = psi_mod_k[:]*np.exp(-1.0j*k_x**2*dt/(2.*m))      

    def _main_loop():
        psi_mod_x[:] = _compute_psi_mod(0)

        for i in range(N-1):
            _x_half_step(i,ft = False)
            _k_full_step()
            _x_half_step(i)
            _compute_psi(i+1)

    _main_loop()

    return psi_x,psi_k,k_x


def oneD_gaussian(x,mean,std,k0):
    return np.exp(-((x-mean)**2)/(4*std**2)+ 1j*x*k0)/(2*np.pi*std**2)**0.25

def V(x):
    V_x = np.zeros_like(x)
    V_x[np.where(abs(x) < 0.5)] = 1.5
    return V_x

N_x = 2**11
dx = 0.05
x = dx * (np.arange(N_x) - 0.5 * N_x)

dt = 0.01
N_t = 2000

p0 = 2.0
d = np.sqrt(N_t*dt/2.)

psi_0 = oneD_gaussian(x,x.max()-10.*d, d, -p0)

psi_x,psi_k,k = split_step_schrodinger(psi_0, dx, dt, V, N_t, x_0 = x[0])