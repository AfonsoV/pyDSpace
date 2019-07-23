


def plot_cross(eixo,x=0,y=0,gap=0.75,size=1.0,color="black",lw=3, alpha=1):
    print(color)
    eixo.plot([x,x],[y-gap,y-gap-size],color=color,lw=lw,alpha=alpha)
    eixo.plot([x,x],[y+gap,y+gap+size],color=color,lw=lw,alpha=alpha)
    eixo.plot([x-gap,x-gap-size],[y,y],color=color,lw=lw,alpha=alpha)
    eixo.plot([x+gap,x+gap+size],[y,y],color=color,lw=lw,alpha=alpha)
    return None
