class EnrollmentMixin(object):

      def is_enrolled(self,user, course_id, catalogue_models):
		  return catalogue_models.Enrollment.objects.filter(user=user,product_id=course_id).exists()
