"""
Blog Graphics and Content Generation Module

This module provides tools for creating publication-quality blog content
for LinkedIn and Substack from EV Pulse NC research data.

Usage:
    from blog import blog_graphics

    # Or import specific functions
    from blog.blog_graphics import (
        create_stat_card,
        create_stat_grid,
        create_social_preview,
        create_comparison_bar,
        create_ev_pulse_hero,
        create_ev_pulse_stats,
    )

Author: Wolfgang Sanyer
License: Polyform Noncommercial 1.0.0 (see LICENSE)
"""

from . import blog_graphics

__all__ = ['blog_graphics']
