from enum import Enum


class JobStatusEnum(str, Enum):
    APPLIED = "Applied"
    OA = "OA"
    INTERVIEW = "Interview"
    REJECTED = "Rejected"
    OFFER = "Offer"
    WISHLIST = "Wishlist"
    OTHER = "Other"


class UserRoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"
