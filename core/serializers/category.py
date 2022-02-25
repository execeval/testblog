from rest_flex_fields import FlexFieldsModelSerializer
import core.models


class PostCategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = core.models.PostCategory
        fields = '__all__'
