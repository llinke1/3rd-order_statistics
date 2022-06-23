import treecorr
from matplotlib.offsetbox import AnchoredText as AT
from helpers_plot import finalizePlot
import numpy as np
import matplotlib.pyplot as plt

def plotTwoPoint(ax, fn_GG, fn_II, fn_GI, binname="", dir_out="./"):
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(r'$\theta$ [arcmin]')
    ax.set_ylabel(r'$\xi_+$')

    TwoPoint=treecorr.GGCorrelation(min_sep=2, max_sep=100, nbins=10, sep_units='arcmin')

    TwoPoint.read(fn_GG)
    ax.plot(TwoPoint.meanr, TwoPoint.xip, label="GG", color='xkcd:red')
    TwoPoint.read(fn_II)
    ax.plot(TwoPoint.meanr, TwoPoint.xip, label="II", color='xkcd:blue')
    TwoPoint.read(fn_GI)
    ax.plot(TwoPoint.meanr, -TwoPoint.xip, label=r"$(-1)\times$GI", color='xkcd:purple')

    
    at=AT(binname, loc='upper right')
    ax.add_artist(at)

    finalizePlot(ax, title="Two-Point Statistics for "+binname, outputFn=dir_out+binname+"_xip.png")


def plotThreePoint(ax,  fns, binlabels, name="", dir_out="./"):
    correlators=[]
    for fn in fns:
        ThreePoint=treecorr.GGGCorrelation(min_sep=2, max_sep=100, nbins=10, nubins=10, nvbins=10, sep_units='arcmin')
        ThreePoint.read(dir_out+fn[:-5]+"_"+name+".dat")
        correlators.append(ThreePoint)

    titlesize = 9
    vsteps=10
    usteps=10
    u_plot = [1,3,5,7,9]
    v_plot = [0,2,4,6,8]
    n_u_plot = len(u_plot)
    n_v_plot = len(v_plot)

    fig,ax = plt.subplots(n_u_plot,n_v_plot,figsize=(10,10),sharey=True,sharex=True)
    plt.subplots_adjust(wspace=0,hspace=0)
    #r_array_const = ThreePoint.meand2[:,9,steps]
    for u_ind_plot_2 in range(n_u_plot):
        for v_ind_plot_2 in range(n_v_plot):
            u_ind_plot = u_plot[u_ind_plot_2]
            v_ind_plot = u_plot[v_ind_plot_2]
            v_ind_plot_treecorr = vsteps+v_ind_plot
            for i, threepoint in enumerate(correlators):
                r_array = threepoint.meand2[:,u_ind_plot,v_ind_plot_treecorr]
                u_array = np.array(threepoint.meanu[:,u_ind_plot,v_ind_plot_treecorr])
                v_array = np.array(threepoint.meanv[:,u_ind_plot,v_ind_plot_treecorr])
                ax[u_ind_plot_2,v_ind_plot_2].plot(r_array,r_array*threepoint.gam0r[:,u_ind_plot,v_ind_plot_treecorr],
                                                label=binlabels[i])


            if(u_ind_plot_2==n_u_plot-1):
                ax[u_ind_plot_2,v_ind_plot_2].set_xlabel('$r$ [arcmin]')
            ax[u_ind_plot_2,v_ind_plot_2].set_xscale('log')
            #ax[u_ind_plot_2,v_ind_plot_2].set_yscale('log')

            ax[u_ind_plot_2,v_ind_plot_2].set_title('$u='+str(round(correlators[0].meanu[5,u_ind_plot,v_ind_plot_treecorr],2))+',\\, v='+str(round(correlators[0].meanv[5,u_ind_plot,v_ind_plot_treecorr],2))+'$'
                                                ,fontsize=titlesize,y=0.86)
            #plot_triangle(ax[u_ind_plot_2,v_ind_plot_2],np.mean(u_array),np.mean(v_array),ypos=0.1,xpos=0.65)
            ax[u_ind_plot_2,v_ind_plot_2].set_xticks([1,10,100])
    ax[0,0].legend(bbox_to_anchor=(6.5,-4.), loc='lower right')
    plt.suptitle(r"$r\times \Re(\Gamma_0)$ for "+name, fontsize=30)

    finalizePlot(ax,  outputFn=dir_out+name+"_gamma0.png", showlegend=False, tightlayout=True)


def plotThreePoint_angle_averaged(ax,  fns, binlabels, name="", dir_out="./"):
    correlators=[]
    for fn in fns:
        ThreePoint=treecorr.GGGCorrelation(min_sep=2, max_sep=100, nbins=10, nubins=10, nvbins=10, sep_units='arcmin')
        ThreePoint.read(dir_out+fn[:-5]+"_"+name+".dat")
        correlators.append(ThreePoint)


    rs=np.geomspace(2, 100, 10)
    ax.set_xscale('log')
    ax.set_xlabel(r'$r$ [arcmin]')
    ax.set_ylabel(r'$\gamma_\mathrm{ttt}$ for '+f"{name}")
    for i, threepoint in enumerate(correlators):
        gamma_averaged=(threepoint.gam0r+threepoint.gam1r+threepoint.gam2r+threepoint.gam3r)*threepoint.weight
        gamma_averaged=np.sum(np.sum(gamma_averaged, axis=2), axis=1)
        gamma_averaged/=4*np.sum(np.sum(threepoint.weight, axis=2), axis=1)
        ax.plot(rs, gamma_averaged, label=binlabels[i])
    finalizePlot(ax,  outputFn=dir_out+name+"_gammaTTT_averaged.png", tightlayout=True)