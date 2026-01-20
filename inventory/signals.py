# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Transaction, StockBalance

# # 1. When a NEW transaction is ADDED
# @receiver(post_save, sender=Transaction)
# def update_stock_on_save(sender, instance, created, **kwargs):
#     if created:
#         balance, _ = StockBalance.objects.get_or_create(
#             godown=instance.godown,
#             crop=instance.crop
#         )
#         if instance.type == 'SR':  # Incoming
#             balance.current_bags += instance.bags
#             balance.current_weight += instance.weight
#         elif instance.type == 'DL':  # Outgoing
#             balance.current_bags -= instance.bags
#             balance.current_weight -= instance.weight
#         balance.save()

# # 2. When a transaction is DELETED (Reverse the math)
# @receiver(post_delete, sender=Transaction)
# def update_stock_on_delete(sender, instance, **kwargs):
#     try:
#         balance = StockBalance.objects.get(
#             godown=instance.godown,
#             crop=instance.crop
#         )
#         # Do the OPPOSITE of what happened
#         if instance.type == 'SR':  # Was Incoming, so we SUBTRACT
#             balance.current_bags -= instance.bags
#             balance.current_weight -= instance.weight
#         elif instance.type == 'DL':  # Was Outgoing, so we ADD back
#             balance.current_bags += instance.bags
#             balance.current_weight += instance.weight
#         balance.save()
#     except StockBalance.DoesNotExist:
#         pass # If stock record is gone, do nothing