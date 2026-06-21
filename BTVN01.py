from abc import ABC, abstractmethod


# ================= BASE ACCOUNT =================
class BaseAccount(ABC):
    bank_name = "Vietcombank"

    def __init__(self, account_number, owner_name, balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def _set_balance(self, amount):
        self.__balance = amount

    @property
    def owner_name(self):
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, name):
        self.__owner_name = " ".join(name.strip().upper().split())

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented
        return self.balance + other.balance

    def __lt__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented
        return self.balance < other.balance

    @staticmethod
    def validate_account_number(account_number):
        return account_number.isdigit() and len(account_number) == 10

    @classmethod
    def update_bank_name(cls, new_name):
        cls.bank_name = new_name


# ================= SAVINGS =================
class SavingsAccount(BaseAccount):

    def __init__(self, account_number, owner_name,
                 interest_rate, balance=0):
        super().__init__(account_number,
                         owner_name,
                         balance)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        self._set_balance(self.balance + amount)

    def withdraw(self, amount):
        fee = amount * 0.02
        total = amount + fee

        if total > self.balance:
            print("Số dư không đủ!")
            return

        self._set_balance(self.balance - total)

        print("Rút tiền thành công!")
        print(f"Số tiền rút: {amount:,.0f} VND")
        print(f"Phí phạt: {fee:,.0f} VND")
        print(f"Số dư còn lại: {self.balance:,.0f} VND")

    def apply_interest(self):
        interest = self.balance * self.interest_rate

        print(f"Tiền lãi nhận được: {interest:,.0f} VND")

        self._set_balance(self.balance + interest)

        print(f"Số dư mới: {self.balance:,.0f} VND")


# ================= CREDIT =================
class CreditAccount(BaseAccount):

    def __init__(self, account_number,
                 owner_name,
                 credit_limit,
                 balance=0):
        super().__init__(account_number,
                         owner_name,
                         balance)
        self.credit_limit = credit_limit

    def deposit(self, amount):
        self._set_balance(self.balance + amount)

    def withdraw(self, amount):

        if self.balance - amount < -self.credit_limit:
            raise ValueError(
                "Vượt quá hạn mức thấu chi cho phép"
            )

        self._set_balance(self.balance - amount)

        print("Rút tiền thành công!")
        print(f"Số dư hiện tại: {self.balance:,.0f} VND")


# ================= MIXIN =================
class DigitalPremiumMixin:

    def cashback_reward(self, amount):

        if amount > 5000000:

            cashback = amount * 0.01

            self._set_balance(
                self.balance + cashback
            )

            print(
                f"[Ưu đãi Premium] Hoàn tiền "
                f"{cashback:,.0f} VND"
            )


# ================= HYBRID =================
class HybridAccount(
    SavingsAccount,
    DigitalPremiumMixin
):

    def deposit(self, amount):
        super().deposit(amount)
        self.cashback_reward(amount)


# ================= GATEWAY =================
class VNPayGateway:

    def execute_pay(self, account, amount):

        account.withdraw(amount)

        print(
            f"[VNPay] Thanh toán "
            f"{amount:,.0f} VND thành công"
        )


class ViettelMoneyGateway:

    def execute_pay(self, account, amount):

        account.withdraw(amount)

        print(
            f"[Viettel Money] Thanh toán "
            f"{amount:,.0f} VND thành công"
        )


# ================= DUCK TYPING =================
def process_payment(
        payment_gateway,
        account,
        amount):

    try:
        payment_gateway.execute_pay(
            account,
            amount
        )

    except AttributeError:
        print(
            "Cổng thanh toán không hợp lệ "
            "hoặc chưa được tích hợp"
        )


# ================= SHOW INFO =================
def show_info(account):

    print("\n--- THÔNG TIN TÀI KHOẢN ---")

    print(
        f"Loại tài khoản: "
        f"{account.__class__.__name__}"
    )

    print(
        f"Ngân hàng: "
        f"{account.bank_name}"
    )

    print(
        f"Số tài khoản: "
        f"{account.account_number}"
    )

    print(
        f"Chủ tài khoản: "
        f"{account.owner_name}"
    )

    print(
        f"Số dư: "
        f"{account.balance:,.0f} VND"
    )

    if isinstance(
            account,
            (SavingsAccount, HybridAccount)
    ):
        print(
            f"Lãi suất: "
            f"{account.interest_rate * 100}%"
        )

    print("\nMRO:")

    for cls in account.__class__.__mro__:
        print(cls.__name__)


# ================= MAIN =================
accounts = []
current_account = None

while True:

    print("\n===== VIETCOMBANK DIGIBANK PRO =====")
    print("1. Mở tài khoản")
    print("2. Xem thông tin & MRO")
    print("3. Nạp / Rút tiền")
    print("4. Tính lãi")
    print("5. Overloading")
    print("6. Thanh toán hóa đơn")
    print("7. Thoát")

    choice = input("Chọn: ")

    # ===== 1 =====
    if choice == "1":

        print("\n1. Savings")
        print("2. Credit")
        print("3. Hybrid")

        acc_type = input("Chọn loại: ")

        account_number = input(
            "Nhập số tài khoản: "
        )

        if not BaseAccount.validate_account_number(
                account_number):
            print(
                "Số tài khoản không hợp lệ!"
            )
            continue

        owner_name = input(
            "Nhập tên chủ tài khoản: "
        )

        if acc_type == "1":

            rate = float(
                input("Lãi suất: ")
            )

            account = SavingsAccount(
                account_number,
                owner_name,
                rate
            )

        elif acc_type == "2":

            limit = float(
                input("Hạn mức tín dụng: ")
            )

            account = CreditAccount(
                account_number,
                owner_name,
                limit
            )

        elif acc_type == "3":

            rate = float(
                input("Lãi suất: ")
            )

            account = HybridAccount(
                account_number,
                owner_name,
                rate
            )

        else:
            print("Lựa chọn không hợp lệ!")
            continue

        accounts.append(account)
        current_account = account

        print("Mở tài khoản thành công!")
        print(
            f"Chủ tài khoản: "
            f"{account.owner_name}"
        )

    # ===== 2 =====
    elif choice == "2":

        if current_account is None:
            print(
                "Chưa có tài khoản!"
            )
        else:
            show_info(current_account)

    # ===== 3 =====
    elif choice == "3":

        if current_account is None:
            print(
                "Chưa có tài khoản!"
            )
            continue

        print("1. Nạp tiền")
        print("2. Rút tiền")

        action = input("Chọn: ")

        amount = float(
            input("Nhập số tiền: ")
        )

        try:

            if action == "1":

                current_account.deposit(
                    amount
                )

                print(
                    f"Số dư mới: "
                    f"{current_account.balance:,.0f}"
                )

            elif action == "2":

                current_account.withdraw(
                    amount
                )

        except ValueError as e:
            print(e)

    # ===== 4 =====
    elif choice == "4":

        if isinstance(
                current_account,
                (SavingsAccount,
                 HybridAccount)
        ):

            current_account.apply_interest()

        else:
            print(
                "Tính năng không hỗ trợ!"
            )

    # ===== 5 =====
    elif choice == "5":

        if len(accounts) < 2:
            print(
                "Cần ít nhất 2 tài khoản!"
            )
            continue

        print(
            "\nDanh sách tài khoản:"
        )

        for i in range(len(accounts)):

            print(
                f"{i}. "
                f"{accounts[i].owner_name}"
            )

        index = int(
            input(
                "Chọn tài khoản đối ứng: "
            )
        )

        other = accounts[index]

        if current_account < other:
            print(
                "Tài khoản hiện tại "
                "nhỏ hơn tài khoản đối ứng"
            )
        else:
            print(
                "Tài khoản hiện tại "
                "lớn hơn hoặc bằng"
            )

        print(
            f"Tổng số dư: "
            f"{current_account + other:,.0f} VND"
        )

    # ===== 6 =====
    elif choice == "6":

        if current_account is None:
            print(
                "Chưa có tài khoản!"
            )
            continue

        print("1. VNPay")
        print("2. Viettel Money")

        gateway_choice = input(
            "Chọn cổng: "
        )

        amount = float(
            input(
                "Nhập số tiền hóa đơn: "
            )
        )

        if gateway_choice == "1":
            gateway = VNPayGateway()

        elif gateway_choice == "2":
            gateway = ViettelMoneyGateway()

        else:
            gateway = object()

        process_payment(
            gateway,
            current_account,
            amount
        )

    # ===== 7 =====
    elif choice == "7":

        print(
            "Cảm ơn đã sử dụng chương trình!"
        )
        break

    else:
        print("Lựa chọn không hợp lệ!")