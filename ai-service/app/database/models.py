from sqlalchemy import (
    Column,
    BigInteger,
    Boolean,
    String,
    Text,
    DateTime,
    ForeignKey,
    DECIMAL
)

from sqlalchemy.sql import func

from app.database.connection import Base


# ============================================
# CONVERSATIONS
# ============================================

class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# ============================================
# MESSAGES
# ============================================

class Message(Base):

    __tablename__ = "messages"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    conversation_id = Column(
        BigInteger,
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# ============================================
# LONG-TERM MEMORY
# ============================================

class Memory(Base):

    __tablename__ = "memories"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        nullable=False,
        index=True
    )

    content = Column(
        Text,
        nullable=False
    )

    memory_type = Column(
        String(50),
        default="GENERAL"
    )

    importance = Column(
        BigInteger,
        default=5
    )

    active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# ============================================
# BANK ACCOUNTS
# Existing demo banking table
# ============================================

class BankAccount(Base):

    __tablename__ = "bank_accounts"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        nullable=False,
        index=True
    )

    account_number = Column(
        String(20),
        nullable=False,
        unique=True
    )

    account_type = Column(
        String(30),
        nullable=False,
        default="SAVINGS"
    )

    balance = Column(
        DECIMAL(15, 2),
        nullable=False,
        default=0.00
    )

    branch_name = Column(
        String(100),
        nullable=True
    )

    ifsc_code = Column(
        String(20),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


# ============================================
# TRANSACTIONS
# Existing demo banking table
# ============================================

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    account_id = Column(
        BigInteger,
        ForeignKey(
            "bank_accounts.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    transaction_type = Column(
        String(20),
        nullable=False
    )

    amount = Column(
        DECIMAL(15, 2),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=True
    )

    transaction_date = Column(
        DateTime,
        server_default=func.now()
    )

# ============================================
# FIXED DEPOSITS
# Existing banking table
# ============================================

class FixedDeposit(Base):

    __tablename__ = "fixed_deposits"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        nullable=False,
        index=True
    )

    principal_amount = Column(
        DECIMAL(15, 2),
        nullable=False
    )

    interest_rate = Column(
        DECIMAL(5, 2),
        nullable=False
    )

    tenure_months = Column(
        BigInteger,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )


# ============================================
# LOANS
# Existing banking table
# ============================================

class Loan(Base):

    __tablename__ = "loans"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        nullable=False,
        index=True
    )

    loan_type = Column(
        String(50),
        nullable=False
    )

    principal_amount = Column(
        DECIMAL(15, 2),
        nullable=False
    )

    interest_rate = Column(
        DECIMAL(5, 2),
        nullable=False
    )

    tenure_months = Column(
        BigInteger,
        nullable=False
    )

    outstanding_amount = Column(
        DECIMAL(15, 2),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )

# ============================================
# CARDS
# Existing banking table
# ============================================

class Card(Base):

    __tablename__ = "cards"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        nullable=False,
        index=True
    )

    card_type = Column(
        String(30),
        nullable=False
    )

    card_number = Column(
        String(30),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )