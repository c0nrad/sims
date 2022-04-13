#include <Eigen/Dense>
#include <Eigen/SparseCore>
#include <complex>
#include <iostream>

using Eigen::SparseMatrix;
using Eigen::VectorXcd;
using namespace std;

typedef Eigen::Triplet<complex<double>> T;

const int N = 5000;
const double L = 1.0e-10;
const double dx = L / N;
const double dt = 1.0e-19;
const double k = 5e11;
const double m = 9.109e-31;
const double sigma = 5.0e-12;
const double x0 = L / 2;
const double hbar = 1.05457183e-34;

double t = 0;

void initialize_gaussian_wave(VectorXcd& in) {
    for (int x = 0; x < N; x++) {
        in(x) = exp(-pow((x * dx) - x0, 2) / (2 * pow(sigma, 2))) * exp(complex<double>(0, -1) * k * complex<double>(x * dx, 0));
    }
}

void initialize_crankNicolson_b(SparseMatrix<complex<double>>& B) {
    complex<double> b1 = complex<double>(1, -dt * hbar / (2 * m * pow(dx, 2)));
    complex<double> b2 = complex<double>(0, dt * hbar / (4 * m * pow(dx, 2)));

    typedef Eigen::Triplet<complex<double>> T;
    std::vector<T> tripletList;
    tripletList.reserve(3 * N);

    tripletList.push_back(T(0, 0, b1));
    tripletList.push_back(T(0, 1, b2));
    tripletList.push_back(T(N - 1, N - 2, b2));
    tripletList.push_back(T(N - 1, N - 1, b1));

    for (int i = 1; i < N - 1; i++) {
        tripletList.push_back(T(i, i - 1, b2));
        tripletList.push_back(T(i, i, b1));
        tripletList.push_back(T(i, i + 1, b2));
    }
    B.setFromTriplets(tripletList.begin(), tripletList.end());
}

void initialize_crankNicolson_a(SparseMatrix<complex<double>>& A) {
    complex<double> a1 = complex<double>(1, dt * hbar / (2 * m * pow(dx, 2)));
    complex<double> a2 = complex<double>(0, -dt * hbar / (4 * m * pow(dx, 2)));

    typedef Eigen::Triplet<complex<double>> T;
    std::vector<T> tripletList;
    tripletList.reserve(3 * N);

    tripletList.push_back(T(0, 0, a1));
    tripletList.push_back(T(0, 1, a2));
    tripletList.push_back(T(N - 1, N - 2, a2));
    tripletList.push_back(T(N - 1, N - 1, a1));

    for (int i = 1; i < N - 1; i++) {
        tripletList.push_back(T(i, i - 1, a2));
        tripletList.push_back(T(i, i, a1));
        tripletList.push_back(T(i, i + 1, a2));
    }
    A.setFromTriplets(tripletList.begin(), tripletList.end());
}

VectorXcd thomasSolve(SparseMatrix<complex<double>> A, VectorXcd v) {
    for (int y = 0; y < A.rows() - 1; y++) {
        // Scale Current Row
        auto scale = A.coeff(y, y);
        v(y) = v(y) / scale;
        A.coeffRef(y, y) = A.coeff(y, y) / scale;
        A.coeffRef(y, y + 1) = A.coeff(y, y + 1) / scale;

        // Subtract From Row Below
        scale = A.coeff(y + 1, y);
        v(y + 1) = v(y + 1) - v(y) * scale;

        A.coeffRef(y + 1, y) = A.coeff(y + 1, y) - A.coeff(y, y) * scale;
        A.coeffRef(y + 1, y + 1) = A.coeff(y + 1, y + 1) - A.coeff(y, y + 1) * scale;
    }

    // Finish last row
    v(A.rows() - 1) = v(A.rows() - 1) / A.coeff(A.rows() - 1, A.rows() - 1);
    A.coeffRef(A.rows() - 1, A.rows() - 1) = 1;

    auto view = A.triangularView<Eigen::UnitUpper>();
    return view.solve(v);
}

void dump_probabilities(VectorXcd out) {
    cout << "# x\tpsi^2" << endl;
    for (int i = 0; i < N; i++) {
        cout << i << "\t" << pow(out(i).real(), 2) + pow(out(i).imag(), 2) << endl;
    }
}

void normalize_psi(VectorXcd& psi) {
    double norm = 0;
    for (int i = 0; i < N; i++) {
        norm += pow(psi(i).real(), 2) + pow(psi(i).imag(), 2);
    }
    psi /= sqrt(norm);
}

VectorXcd step(VectorXcd& psi, const SparseMatrix<complex<double>>& A, const SparseMatrix<complex<double>>& B) {
    VectorXcd v = B * psi;

    // cout << "IS Approx? " << A.toDense().colPivHouseholderQr().solve(v).isApprox(thomasSolve(A, v)) << endl;
    // cout << "Official: " << A.toDense().colPivHouseholderQr().solve(v) << endl;
    // cout << "Thomas: " << thomasSolve(A, v) << endl;

    return thomasSolve(A, v);
}

int main() {
    VectorXcd psi(N);
    initialize_gaussian_wave(psi);
    normalize_psi(psi);

    SparseMatrix<complex<double>>
        A(N, N);
    SparseMatrix<complex<double>> B(N, N);

    initialize_crankNicolson_a(A);
    initialize_crankNicolson_b(B);

    for (int i = 0; i < 500; i++) {
        dump_probabilities(psi);
        cout << "\n"
             << endl;
        psi = step(psi, A, B);
    }
}
