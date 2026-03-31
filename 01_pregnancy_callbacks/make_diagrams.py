"""
Generate diagrams for the Starsim show-and-tell presentation on hooks and callbacks.

Run:  python make_diagrams.py
Produces: loop_order.png, hooks_vs_inheritance.png, pregnancy_hooks.png
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
import numpy as np

# --------------------------------------------------------------------------
# Shared styling
# --------------------------------------------------------------------------
COLORS = dict(
    sim      = '#94a3b8',  # slate
    custom   = '#a78bfa',  # violet
    demog    = '#f97316',  # orange
    disease  = '#ef4444',  # red
    connect  = '#8b5cf6',  # purple
    network  = '#3b82f6',  # blue
    intv     = '#22c55e',  # green
    people   = '#64748b',  # grey
    analyzer = '#eab308',  # yellow
    hook     = '#ec4899',  # pink / magenta
    inherit  = '#0ea5e9',  # sky blue
    bg       = '#f8fafc',  # light bg
)

def styled_box(ax, x, y, w, h, text, color, fontsize=10, alpha=0.85, text_color='white', bold=False):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle='round,pad=0.08', facecolor=color, edgecolor='white',
                         linewidth=1.5, alpha=alpha, zorder=2)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=text_color, weight=weight, zorder=3)
    return box


def arrow(ax, x1, y1, x2, y2, color='#334155', lw=1.5, style='->', shrink=4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                shrinkA=shrink, shrinkB=shrink),
                zorder=1)


# ==========================================================================
# DIAGRAM 1 : Loop order of operations
# ==========================================================================
def make_loop_diagram():
    fig, ax = plt.subplots(figsize=(5, 11))
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-0.5, 17)
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor(COLORS['bg'])
    ax.axis('off')

    steps = [
        ('1.  sim.start_step()',          COLORS['sim']),
        ('2.  modules.start_step()',      COLORS['sim']),
        ('3.  custom.step()',             COLORS['custom']),
        ('4.  demographics.step()',       COLORS['demog']),
        ('5.  diseases.step_state()',     COLORS['disease']),
        ('6.  connectors.step()',         COLORS['connect']),
        ('7.  networks.step()',           COLORS['network']),
        ('8.  interventions.step()',      COLORS['intv']),
        ('9.  diseases.step()',           COLORS['disease']),
        ('10. people.step_die()',         COLORS['people']),
        ('11. people.update_results()',   COLORS['people']),
        ('12. modules.update_results()',  COLORS['sim']),
        ('13. analyzers.step()',          COLORS['analyzer']),
        ('14. modules.finish_step()',     COLORS['sim']),
        ('15. people.finish_step()',      COLORS['people']),
        ('16. sim.finish_step()',         COLORS['sim']),
    ]

    w, h = 3.6, 0.65
    x0 = 0
    y_top = 16.2

    for i, (label, color) in enumerate(steps):
        y = y_top - i * (h + 0.32)
        styled_box(ax, x0, y, w, h, label, color, fontsize=9)
        if i < len(steps) - 1:
            arrow(ax, x0, y - h/2, x0, y - h/2 - 0.32, lw=1.2)

    ax.set_title('Starsim loop: order of operations\n(one timestep)', fontsize=13, weight='bold', pad=15)
    fig.tight_layout()
    fig.savefig('loop_order.png', dpi=180, bbox_inches='tight', facecolor=COLORS['bg'])
    print('Saved loop_order.png')
    plt.close(fig)


# ==========================================================================
# DIAGRAM 2 : Inheritance vs hooks — two ways to extend a module
# ==========================================================================
def make_hooks_vs_inheritance():
    fig, axes = plt.subplots(1, 2, figsize=(13, 7.5))
    fig.patch.set_facecolor(COLORS['bg'])

    for ax in axes:
        ax.set_facecolor(COLORS['bg'])
        ax.axis('off')

    w, h = 4.0, 0.65
    gap = 0.35

    # ---- Left panel: inheritance ----
    ax = axes[0]
    ax.set_xlim(-3, 3)
    ax.set_ylim(-1.5, 9)
    ax.set_title('Approach A: inheritance', fontsize=13, weight='bold', pad=10)

    # Base class
    base_steps = [
        ('class SIR(Infection)',     COLORS['disease']),
        ('  step_state()',           COLORS['disease']),
        ('  set_prognoses()',        COLORS['disease']),
    ]
    y = 8.0
    for i, (label, color) in enumerate(base_steps):
        styled_box(ax, 0, y, w, h, label, color, fontsize=9.5)
        if i < len(base_steps) - 1:
            arrow(ax, 0, y - h/2, 0, y - h/2 - gap, lw=1.2)
        y -= (h + gap)

    # Arrow down to subclass
    ax.annotate('inherits', xy=(0, y + 0.15), xytext=(0, y + 0.55),
                fontsize=9, ha='center', color='#64748b',
                arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.5))
    y -= 0.3

    sub_steps = [
        ('class SIRWithViralLoad(SIR)', COLORS['inherit']),
        ('  step_state()  # override',  COLORS['inherit']),
        ('  set_prognoses()  # override', COLORS['inherit']),
        ('  update_viral_load()',        COLORS['inherit']),
    ]
    for i, (label, color) in enumerate(sub_steps):
        styled_box(ax, 0, y, w, h, label, color, fontsize=9)
        if i < len(sub_steps) - 1:
            arrow(ax, 0, y - h/2, 0, y - h/2 - gap, lw=1.2, color=COLORS['inherit'])
        y -= (h + gap)

    ax.text(0, -1.0, 'Everything in one class\nMust override carefully', ha='center',
            fontsize=9, style='italic', color='#64748b')

    # ---- Right panel: hooks ----
    ax = axes[1]
    ax.set_xlim(-5, 5)
    ax.set_ylim(-1.5, 9)
    ax.set_title('Approach B: hooks (callbacks)', fontsize=13, weight='bold', pad=10)

    # Base class with hooks
    x_base = -1.5
    w_base = 3.5
    base_hook_steps = [
        ('class SIR(Infection)',        COLORS['disease']),
        ('  step_state()',              COLORS['disease']),
        ('  set_prognoses()',           COLORS['disease']),
        ('    >> infection callbacks >>', COLORS['hook']),
    ]
    y = 8.0
    for i, (label, color) in enumerate(base_hook_steps):
        is_hook = '>>' in label
        bw = w_base - 0.3 if is_hook else w_base
        styled_box(ax, x_base, y, bw, h, label.strip(), color, fontsize=9,
                   bold=is_hook)
        if i < len(base_hook_steps) - 1:
            arrow(ax, x_base, y - h/2, x_base, y - h/2 - gap, lw=1.2)
        y -= (h + gap)

    # Separate module on the right
    x_ext = 2.8
    w_ext = 3.2
    ext_steps = [
        ('class ViralLoadTracker(Module)', COLORS['hook']),
        ('  on_infection(uids)',            COLORS['hook']),
        ('  update_viral_load()',           COLORS['hook']),
    ]
    ey = 8.0 - 1 * (h + gap)  # Start aligned with step_state
    for i, (label, color) in enumerate(ext_steps):
        styled_box(ax, x_ext, ey, w_ext, h, label, color, fontsize=9)
        if i < len(ext_steps) - 1:
            arrow(ax, x_ext, ey - h/2, x_ext, ey - h/2 - gap, lw=1.2, color=COLORS['hook'])
        ey -= (h + gap)

    # Hook arrow from base to extension
    hook_y = 8.0 - 3 * (h + gap)  # y of the callback row
    arrow(ax, x_base + w_base/2, hook_y, x_ext - w_ext/2, 8.0 - 1 * (h + gap),
          color=COLORS['hook'], lw=2.5)

    # "registers" label
    ax.annotate('registers at init', xy=(x_base + w_base/2 - 0.2, hook_y + 0.5),
                xytext=(x_ext - 0.3, hook_y + 1.2),
                fontsize=8, ha='center', color=COLORS['hook'], style='italic',
                arrowprops=dict(arrowstyle='->', color=COLORS['hook'], lw=1, linestyle='--'))

    ax.text(0.5, -1.0, 'Two separate modules\nBase class unchanged', ha='center',
            fontsize=9, style='italic', color='#64748b')

    fig.suptitle('Two ways to extend a module', fontsize=15, weight='bold', y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig('hooks_vs_inheritance.png', dpi=180, bbox_inches='tight', facecolor=COLORS['bg'])
    print('Saved hooks_vs_inheritance.png')
    plt.close(fig)


# ==========================================================================
# DIAGRAM 3 : Inside Pregnancy.step() — hooks to FetalHealth
# ==========================================================================
def make_pregnancy_hooks_diagram():
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-1, 13)
    ax.set_facecolor(COLORS['bg'])
    fig.patch.set_facecolor(COLORS['bg'])
    ax.axis('off')

    w, h = 3.5, 0.55
    gap = 0.2
    x_left = -2.2
    x_right = 2.2

    # Column headers
    ax.text(x_left, 12.5, 'Pregnancy.step()', ha='center', fontsize=12,
            weight='bold', color=COLORS['demog'])
    ax.text(x_right, 12.5, 'FetalHealth', ha='center', fontsize=12,
            weight='bold', color=COLORS['hook'])

    # Pregnancy substeps
    preg_steps = [
        'Process deliveries',
        '  transfer gestation data',
        '  classify preterm',
        '  update networks',
        '  >> delivery callbacks >>',
        'Select conceivers',
        'Make pregnancies & embryos',
        '  >> conception callbacks >>',
        'Add embryos to networks',
        'Update maternal deaths',
    ]

    y = 11.8
    preg_ys = []
    for i, step in enumerate(preg_steps):
        is_callback = '>>' in step
        is_sub = step.startswith('  ') and not is_callback
        color = COLORS['hook'] if is_callback else ('#fdba74' if is_sub else COLORS['demog'])
        fontsize = 9 if is_sub else 9.5
        bw = w if not is_sub else w - 0.3
        styled_box(ax, x_left, y, bw, h, step.strip(), color, fontsize=fontsize,
                   bold=is_callback)
        preg_ys.append(y)
        if i < len(preg_steps) - 1:
            arrow(ax, x_left, y - h/2, x_left, y - h/2 - gap, color='#94a3b8', lw=1)
        y -= (h + gap)

    # FetalHealth: on_delivery
    delivery_y = preg_ys[4]
    fh_delivery_steps = [
        'compute_birth_weight()',
        'classify LBW / SGA / SVN',
        'store on newborns',
    ]
    fy = delivery_y + 0.5
    for i, step in enumerate(fh_delivery_steps):
        styled_box(ax, x_right, fy, w, h * 0.9, step, COLORS['hook'], fontsize=8.5)
        if i < len(fh_delivery_steps) - 1:
            arrow(ax, x_right, fy - h*0.9/2, x_right, fy - h*0.9/2 - gap*0.8,
                  color=COLORS['hook'], lw=1)
        fy -= (h * 0.9 + gap * 0.8)

    # FetalHealth: on_conception
    conception_y = preg_ys[7]
    fh_conception_steps = [
        'draw weight_percentile',
        'reset growth_restriction',
        'reset timing_shift',
    ]
    fy = conception_y + 0.3
    for i, step in enumerate(fh_conception_steps):
        styled_box(ax, x_right, fy, w, h * 0.9, step, COLORS['hook'], fontsize=8.5)
        if i < len(fh_conception_steps) - 1:
            arrow(ax, x_right, fy - h*0.9/2, x_right, fy - h*0.9/2 - gap*0.8,
                  color=COLORS['hook'], lw=1)
        fy -= (h * 0.9 + gap * 0.8)

    # Hook arrows
    arrow(ax, x_left + w/2, preg_ys[4], x_right - w/2, delivery_y + 0.5,
          color=COLORS['hook'], lw=2.5)
    arrow(ax, x_left + w/2, preg_ys[7], x_right - w/2, conception_y + 0.3,
          color=COLORS['hook'], lw=2.5)

    ax.set_title('Inside Pregnancy.step(): hooks to FetalHealth',
                 fontsize=13, weight='bold', pad=15)
    fig.tight_layout()
    fig.savefig('pregnancy_hooks.png', dpi=180, bbox_inches='tight', facecolor=COLORS['bg'])
    print('Saved pregnancy_hooks.png')
    plt.close(fig)


if __name__ == '__main__':
    make_loop_diagram()
    make_hooks_vs_inheritance()
    make_pregnancy_hooks_diagram()
    print('Done!')
