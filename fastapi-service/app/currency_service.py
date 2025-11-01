"""Currency conversion service implementation."""

# Exchange rates (mock data - in production, fetch from external API)
EXCHANGE_RATES = {
    ('USD', 'EUR'): 0.85,
    ('EUR', 'USD'): 1.18,
    ('USD', 'GBP'): 0.73,
    ('GBP', 'USD'): 1.37,
    ('EUR', 'GBP'): 0.86,
    ('GBP', 'EUR'): 1.16,
}


def convert_currency(from_currency: str, to_currency: str, amount: float) -> dict:
    """    
    Args:
        from_currency: Source currency code
        to_currency: Target currency code
        amount: Amount to convert
    
    Returns:
        Dictionary with converted_amount, rate, and message
    """
    # Normalize currency codes to uppercase
    from_curr = from_currency.upper()
    to_curr = to_currency.upper()
    
    # Same currency
    if from_curr == to_curr:
        return {
            'converted_amount': amount,
            'rate': 1.0,
            'message': f'No conversion needed ({from_curr} to {to_curr})'
        }
    
    # Check direct rate
    rate_key = (from_curr, to_curr)
    if rate_key in EXCHANGE_RATES:
        rate = EXCHANGE_RATES[rate_key]
        converted = amount * rate
        return {
            'converted_amount': converted,
            'rate': rate,
            'message': f'Converted {amount} {from_curr} to {converted:.2f} {to_curr}'
        }
    
    # Try reverse rate
    reverse_key = (to_curr, from_curr)
    if reverse_key in EXCHANGE_RATES:
        rate = 1.0 / EXCHANGE_RATES[reverse_key]
        converted = amount * rate
        return {
            'converted_amount': converted,
            'rate': rate,
            'message': f'Converted {amount} {from_curr} to {converted:.2f} {to_curr}'
        }
    
    # Rate not found
    return {
        'converted_amount': 0.0,
        'rate': 0.0,
        'message': f'Exchange rate not available for {from_curr} to {to_curr}'
    }

