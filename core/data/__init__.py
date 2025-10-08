"""
Data package for BedBees application.
Contains countries data and attractions data extracted from views.py
"""

from .countries_data import countries_data
from .demo_attractions import demo_attractions

__all__ = ['countries_data', 'demo_attractions']
