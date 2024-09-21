from rest_framework import permissions

class IsAdminOrCustomer(permissions.BasePermission):
    """
    Only admins or users associated with the customer profile can access a customer(s)
    """
    def has_permission(self, request, view):
        # user must be autheticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # superuser or user associated with the profile has full access
        return request.user.is_superuser or obj.user == request.user
        
class IsAdminOrOwnOrder(permissions.BasePermission):
    """
    Allows admins full access to orders and customers to their orders only.
    """

    def has_permission(self, request, view):
        # user must be authenticated
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # superusers have full order acess
        if request.user.is_superuser:
            return True
        
        # customers can only update(cancel) their orders
        if request.method in ['GET','PUT', 'PATCH'] and obj.customer.user == request.user:
            return True