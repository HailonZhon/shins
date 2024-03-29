from app.models.redis_config import redis_client
from app.services.user_services.verification_service import get_stored_verification_code


async def validate_verification_code(phone_number: str, input_code: str) -> bool:
    """
    验证给定手机号的验证码是否正确。

    :param phone_number: 用户的手机号码。
    :param input_code: 用户输入的验证码。
    :return: 验证码正确返回 True，否则返回 False。
    """
    try:
        # 从 Redis 中获取存储的验证码
        stored_code = get_stored_verification_code(phone_number)
        print("veryfiy",stored_code,phone_number,input_code)
        # 验证验证码是否匹配且未过期
        if (
            stored_code and stored_code == input_code
        ):  # 确保从 Redis 获取的 bytes 类型数据被转换为 str 类型
            # 验证成功后，清除 Redis 中的验证码，以防重复使用
            redis_client.delete(phone_number)
            return True
        else:
            return False
    except Exception as e:
        # 日志记录异常信息，此处仅为打印，实际应用中可能需要使用 logging 模块记录到文件或监控系统
        print(f"Error validating verification code for {phone_number}: {e}")
        return False  # 如果你希望即使出现异常也按验证失败处理
