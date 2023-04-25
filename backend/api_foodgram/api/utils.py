from rest_framework import response, status


def add_or_remove_from_profile(request, field, object, serializer_data):
    """
    Add or remove object from user profile m2m field.
    """
    if request.method == 'POST':
        field.add(object)
        return response.Response(
            serializer_data,
            status=status.HTTP_201_CREATED
        )
    if request.method == 'DELETE':
        field.remove(object)
        return response.Response(status=status.HTTP_204_NO_CONTENT)