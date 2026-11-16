
import streamlit as st
import secrets
from sympy import randprime, isprime

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Tonelli-Shanks Calculator",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Tonelli–Shanks Calculator")
st.subheader("Group 12: Quadratic Residuosity")
st.write("Modular Square Root Problem: x² ≡ a (mod p)")

st.divider()


# -------------------------------
# EULER'S CRITERION
# -------------------------------

def euler_criterion(a, p):
    a %= p

    if a == 0:
        return 0

    result = pow(a, (p - 1) // 2, p)

    if result == 1:
        return 1
    elif result == p - 1:
        return -1


# -------------------------------
# TONELLI-SHANKS
# -------------------------------

def tonelli_shanks(a, p):
    a %= p

    if p == 2:
        return a

    if a == 0:
        return 0

    if euler_criterion(a, p) != 1:
        return None

    q = p - 1
    s = 0

    while q % 2 == 0:
        q //= 2
        s += 1

    z = 2

    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    c = pow(z, q, p)
    x = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)
    m = s

    while t != 1:
        i = 1
        temp = pow(t, 2, p)

        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1

        b = pow(c, 1 << (m - i - 1), p)

        x = (x * b) % p
        t = (t * b * b) % p
        c = pow(b, 2, p)
        m = i

    return x


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("⚙️ Settings")

# Initialize input values
if "p_text" not in st.session_state:
    st.session_state.p_text = "41"

if "a_text" not in st.session_state:
    st.session_state.a_text = "18"

# Generate a 512-bit prime
if st.sidebar.button("Generate 512-bit Prime"):
    st.session_state.p_text = str(
        randprime(2**511, 2**512)
    )

st.sidebar.info(
    "Use a prime modulus p and enter the value a."
)


# -------------------------------
# USER INPUT
# -------------------------------

st.header("1. Enter Input Values")

col1, col2 = st.columns(2)

with col1:
    p_text = st.text_input(
        "Prime Number (p)",
        key="p_text"
    )

with col2:
    a_text = st.text_input(
        "Number (a)",
        key="a_text"
    )

st.caption(
    "For a 512-bit prime, use the Generate 512-bit Prime button."
)


# -------------------------------
# CALCULATION
# -------------------------------

if st.button("🚀 Calculate Square Root", type="primary"):

    try:
        p = int(p_text.strip())
        a = int(a_text.strip())

    except ValueError:
        st.error("Please enter valid integer values for p and a.")

    else:

        if p < 2:
            st.error("p must be greater than or equal to 2.")

        elif not isprime(p):
            st.error("p must be a prime number.")

        else:

            a = a % p

            st.divider()
            st.header("2. Euler's Criterion")

            result = euler_criterion(a, p)

            if result == 1:
                st.success("Quadratic Residue (QR)")

            elif result == -1:
                st.warning("Quadratic Non-Residue (QNR)")

            else:
                st.info("Zero modulo p")

            st.write(f"Euler result: {result}")

            st.divider()
            st.header("3. Tonelli–Shanks Algorithm")

            if result == -1:

                st.error(
                    "No modular square root exists."
                )

            else:

                root1 = tonelli_shanks(a, p)
                root2 = (-root1) % p

                st.success("Square roots calculated!")

                c1, c2 = st.columns(2)

                with c1:
                    st.metric(
                        "First Root",
                        str(root1)
                    )

                with c2:
                    st.metric(
                        "Second Root",
                        str(root2)
                    )

                st.divider()
                st.header("4. Root Verification")

                v1 = pow(root1, 2, p) == a
                v2 = pow(root2, 2, p) == a

                st.write(
                    "First Root Verification:",
                    "✅ PASS" if v1 else "❌ FAIL"
                )

                st.write(
                    "Second Root Verification:",
                    "✅ PASS" if v2 else "❌ FAIL"
                )

            st.divider()
            st.header("5. Factorization of p-1")

            q = p - 1
            s = 0

            while q % 2 == 0:
                q //= 2
                s += 1

            st.latex(
                rf"p-1 = 2^{{{s}}} \times {q}"
            )

            col1, col2 = st.columns(2)

            col1.metric("Value of s", s)
            col2.metric("Odd value q", str(q))


# -------------------------------
# ADDITIONAL TEST CASES
# -------------------------------

st.divider()
st.header("6. Additional QR and QNR Testing")

if st.button("Generate Test Cases"):

    try:
        p_test = int(p_text.strip())

    except ValueError:
        st.error("Please enter a valid prime p.")

    else:

        if p_test < 5:
            st.warning(
                "Please use a prime p greater than or equal to 5 "
                "to generate two distinct QR and QNR test cases."
            )

        elif not isprime(p_test):
            st.error("Please enter a prime p.")

        else:

            residues = set()
            non_residues = set()

            # Generate two distinct quadratic residues
            while len(residues) < 2:
                r = secrets.randbelow(p_test - 1) + 1
                a1 = pow(r, 2, p_test)
                residues.add(a1)

            # Generate two distinct quadratic non-residues
            while len(non_residues) < 2:
                a1 = secrets.randbelow(p_test - 1) + 1

                if euler_criterion(a1, p_test) == -1:
                    non_residues.add(a1)

            st.subheader("Quadratic Residues")

            for a1 in sorted(residues):

                x = tonelli_shanks(a1, p_test)
                y = (-x) % p_test

                st.write("Residue:", a1)
                st.write("Roots:", x, "and", y)

                st.write(
                    "Verified:",
                    pow(x, 2, p_test) == a1
                    and pow(y, 2, p_test) == a1
                )

                st.divider()

            st.subheader("Quadratic Non-Residues")

            for a1 in sorted(non_residues):

                st.write("Non-Residue:", a1)

                st.write(
                    "Euler Result:",
                    euler_criterion(a1, p_test)
                )

                st.write("Square root does not exist.")

                st.divider()


# -------------------------------
# FOOTER
# -------------------------------

st.caption(
    "Group 12 | Number Theory and Cryptography | "
    "Python + Streamlit"
)
