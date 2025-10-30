from app_account.models import Feedback
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout
from django.forms import ModelForm


class FeedbackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_error_message = "Trường này là bắt buộc phải nhập"
        for field_name, field in self.fields.items():
            if field.required:
                field.error_messages["required"] = required_error_message

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_show_labels = False
        helper.form_method = "post"
        helper.layout = Layout(
            Field(
                "full_name",
                placeholder="Họ và tên *",
                template="custom-crispy/custom-field.html",
                autocomplete="off",
            ),
            Field(
                "email",
                placeholder="E-mail *",
                template="custom-crispy/custom-field.html",
                autocomplete="off",
            ),
            Field(
                "phone",
                placeholder="Số điện thoại",
                template="custom-crispy/custom-field.html",
                autocomplete="off",
            ),
            Field(
                "message",
                placeholder="Tin nhắn *",
                template="custom-crispy/custom-field.html",
                style="resize:none",
                rows="5",
            ),
            Div(
                HTML(
                    "<button type='submit' class='btn button-color-accent d-flex align-items-center gap-2'>"
                    "Gửi <i class='bi bi-send'></i>"
                    "</button>"
                ),
                css_class="mt-2",
            ),
        )
        return helper

    class Meta:
        model = Feedback
        fields = ["full_name", "email", "phone", "message"]
        error_messages = {
            "email": {
                "invalid": "Địa chỉ Email không hợp lệ",
            },
        }
