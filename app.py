
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

    result = pow(a, (p-1)//2, p)

    if result == 1:
        return 1

    elif result == p-1:
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

    while pow(z, (p-1)//2, p) != p-1:
        z += 1

    c = pow(z, q, p)
    x = pow(a, (q+1)//2, p)
    t = pow(a, q, p)
    m = s

    while t != 1:

        i = 1
        temp = pow(t, 2, p)

        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1

        b = pow(c, 1 << (m-i-1), p)

        x = (x*b) % p
        t = (t*b*b) % p
        c = pow(b, 2, p)
        m = i

    return x


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("⚙️ Settings")

if st.sidebar.button("Generate 512-bit Prime"):
    st.session_state.p = int(
        randprime(2**511, 2**512)
    )

if "p" not in st.session_state:
    st.session_state.p = 41

if "a" not in st.session_state:
    st.session_state.a = 18

st.sidebar.info(
    "Use a prime modulus p and enter the value a."
)


# -------------------------------
# USER INPUT
# -------------------------------

st.header("1. Enter Input Values")

col1, col2 = st.columns(2)

with col1:
    p = st.number_input(
        "Prime Number (p)",
        min_value=2,
        value=int(st.session_state.p),
        step=1
    )

with col2:
    a = st.number_input(
        "Number (a)",
        min_value=0,
        value=int(st.session_state.a),
        step=1
    )

st.caption("For a 512-bit prime, use the Generate 512-bit Prime button.")


# -------------------------------
# CALCULATION
# -------------------------------

if st.button("🚀 Calculate Square Root", type="primary"):

    p = int(p)
    a = int(a)

    if not isprime(p):
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

        st.write(
            f"Euler result: {result}"
        )

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

        q = p-1
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

    p = int(p)

    if not isprime(p):
        st.error("Please enter a prime p.")

    else:

        residues = []
        non_residues = []

        while len(residues) < 2:
            r = secrets.randbelow(p-1) + 1
            a1 = pow(r, 2, p)

            if a1 not in residues:
                residues.append(a1)

        while len(non_residues) < 2:
            a1 = secrets.randbelow(p-1) + 1

            if (
                euler_criterion(a1, p) == -1
                and a1 not in non_residues
            ):
                non_residues.append(a1)

        st.subheader("Quadratic Residues")

        for a1 in residues:
            x = tonelli_shanks(a1, p)
            y = (-x) % p

            st.write("Residue:", a1)
            st.write("Roots:", x, "and", y)
            st.write(
                "Verified:",
                pow(x, 2, p) == a1 and
                pow(y, 2, p) == a1
            )
            st.divider()

        st.subheader("Quadratic Non-Residues")

        for a1 in non_residues:
            st.write("Non-Residue:", a1)
            st.write(
                "Euler Result:",
                euler_criterion(a1, p)
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
