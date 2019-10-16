from livestream import models
from catalogue import models as catalogue_models
from custom_user import models as user_models


class CourseRoomMixin(object):

    def get_identity(self,request):

        return "{0}/{1} {2}".format(request.user.email,request.user.first_name,request.user.last_name)


    def get_owner(self,course_id):

        course = catalogue_models.Product.objects.filter(pk=course_id).first()
        owner = user_models.User.objects.filter(pk=course.user_id).first()

        return owner

    def is_owner(self,request, course):
        """
        check if user owns course
        """
        return request.user.pk == course.user_id

    def room_exists(self,course_id):
        return models.TwilioRoom.objects.filter(name=course_id,twilio_room_status__name="Active").exists()
