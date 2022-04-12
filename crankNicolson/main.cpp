#include <Eigen/Dense>
#include <Eigen/SparseCore>
#include <complex>
#include <iostream>

using Eigen::SparseMatrix;
using Eigen::VectorXcd;

using namespace std;

const int N = 5000;
const double L = 1.0e-10;
const double dx = L / N;
const double dt = 1.0e-18;
const double k = 5e10;
const double m = 9.109e-31;
const double sigma = 1.0e-10;
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

    B.insert(0, 0) = b1;
    B.insert(0, 1) = b2;
    B.insert(N - 1, N - 2) = b2;
    B.insert(N - 1, N - 1) = b1;

    for (int i = 1; i < N - 1; i++) {
        B.insert(i, i - 1) = b2;
        B.insert(i, i) = b1;
        B.insert(i, i + 1) = b2;
    }
}

void initialize_crankNicolson_a(SparseMatrix<complex<double>>& A) {
    complex<double> a1 = complex<double>(1, dt * hbar / (2 * m * pow(dx, 2)));
    complex<double> a2 = complex<double>(0, -dt * hbar / (4 * m * pow(dx, 2)));

    A.insert(0, 0) = a1;
    A.insert(0, 1) = a2;
    A.insert(N - 1, N - 2) = a2;
    A.insert(N - 1, N - 1) = a1;

    for (int i = 1; i < N - 1; i++) {
        A.insert(i, i - 1) = a2;
        A.insert(i, i) = a1;
        A.insert(i, i + 1) = a2;
    }
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

VectorXcd step(VectorXcd& psi, SparseMatrix<complex<double>>& A, const SparseMatrix<complex<double>>& B) {
    VectorXcd v = B * psi;
    return thomasSolve(A, v);
}

int main() {
    VectorXcd psi(N);
    initialize_gaussian_wave(psi);

    SparseMatrix<complex<double>> A(N, N);
    SparseMatrix<complex<double>> B(N, N);

    initialize_crankNicolson_a(A);
    initialize_crankNicolson_b(B);

    for (int i = 0; i < 100; i++) {
        cout << i << endl;
        psi = step(psi, A, B);
    }
}
