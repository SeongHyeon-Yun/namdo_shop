def wallet_balance(request):
    if request.user.is_authenticated:
        wallet = getattr(request.user, "wallet", None)
        return {"wallet_balance": wallet.balance if wallet else 0}
    return {}
