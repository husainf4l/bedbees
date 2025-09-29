"use client";

import { useState } from "react";
import {
  CreditCardIcon,
  PlusIcon,
  CheckCircleIcon,
  ClockIcon,
  ArrowDownTrayIcon,
  MagnifyingGlassIcon,
  TrashIcon,
  PencilIcon,
  ShieldCheckIcon,
  BanknotesIcon,
  DocumentTextIcon,
} from "@heroicons/react/24/outline";

interface PaymentMethod {
  id: string;
  type: "credit_card" | "debit_card" | "paypal" | "bank_account";
  isDefault: boolean;
  cardNumber: string;
  expiryDate: string;
  cardHolder: string;
  brand: "visa" | "mastercard" | "amex" | "discover";
  isActive: boolean;
}

interface Transaction {
  id: string;
  type: "payment" | "refund" | "fee";
  status: "completed" | "pending" | "failed" | "cancelled";
  amount: number;
  currency: string;
  description: string;
  date: string;
  paymentMethod: string;
  bookingReference?: string;
}

interface Invoice {
  id: string;
  invoiceNumber: string;
  amount: number;
  currency: string;
  date: string;
  status: "paid" | "pending" | "overdue";
  dueDate: string;
  description: string;
}

const paymentMethods: PaymentMethod[] = [
  {
    id: "1",
    type: "credit_card",
    isDefault: true,
    cardNumber: "**** **** **** 4242",
    expiryDate: "12/26",
    cardHolder: "John Doe",
    brand: "visa",
    isActive: true,
  },
  {
    id: "2",
    type: "credit_card",
    isDefault: false,
    cardNumber: "**** **** **** 8888",
    expiryDate: "08/25",
    cardHolder: "John Doe",
    brand: "mastercard",
    isActive: true,
  },
  {
    id: "3",
    type: "paypal",
    isDefault: false,
    cardNumber: "john.doe@email.com",
    expiryDate: "",
    cardHolder: "John Doe",
    brand: "visa",
    isActive: true,
  },
];

const transactions: Transaction[] = [
  {
    id: "1",
    type: "payment",
    status: "completed",
    amount: 120.0,
    currency: "USD",
    description: "Petra Day Trip from Amman",
    date: "2024-11-20",
    paymentMethod: "**** 4242",
    bookingReference: "BK-2024-001",
  },
  {
    id: "2",
    type: "payment",
    status: "pending",
    amount: 450.0,
    currency: "USD",
    description: "Dead Sea Resort - 3 nights",
    date: "2024-11-25",
    paymentMethod: "**** 8888",
    bookingReference: "BK-2024-002",
  },
  {
    id: "3",
    type: "refund",
    status: "completed",
    amount: 85.0,
    currency: "USD",
    description: "Wadi Rum Desert Safari (Cancelled)",
    date: "2024-11-15",
    paymentMethod: "**** 4242",
    bookingReference: "BK-2024-003",
  },
  {
    id: "4",
    type: "fee",
    status: "completed",
    amount: 5.5,
    currency: "USD",
    description: "Processing Fee",
    date: "2024-11-20",
    paymentMethod: "**** 4242",
  },
];

const invoices: Invoice[] = [
  {
    id: "1",
    invoiceNumber: "INV-2024-001",
    amount: 120.0,
    currency: "USD",
    date: "2024-11-20",
    status: "paid",
    dueDate: "2024-12-20",
    description: "Petra Day Trip from Amman",
  },
  {
    id: "2",
    invoiceNumber: "INV-2024-002",
    amount: 450.0,
    currency: "USD",
    date: "2024-11-25",
    status: "pending",
    dueDate: "2024-12-25",
    description: "Dead Sea Resort - 3 nights",
  },
];

const statusConfig = {
  completed: { color: "text-green-700 bg-green-100", label: "Completed" },
  pending: { color: "text-yellow-700 bg-yellow-100", label: "Pending" },
  failed: { color: "text-red-700 bg-red-100", label: "Failed" },
  cancelled: { color: "text-gray-700 bg-gray-100", label: "Cancelled" },
  paid: { color: "text-green-700 bg-green-100", label: "Paid" },
  overdue: { color: "text-red-700 bg-red-100", label: "Overdue" },
};

export default function Payments() {
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedPeriod, setSelectedPeriod] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  const formatPrice = (amount: number, currency: string) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency,
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const getBrandIcon = (brand: string) => {
    const baseClasses = "w-8 h-8 rounded";
    switch (brand) {
      case "visa":
        return (
          <div
            className={`${baseClasses} bg-blue-600 text-white flex items-center justify-center text-xs font-bold`}
          >
            VISA
          </div>
        );
      case "mastercard":
        return (
          <div
            className={`${baseClasses} bg-red-600 text-white flex items-center justify-center text-xs font-bold`}
          >
            MC
          </div>
        );
      case "amex":
        return (
          <div
            className={`${baseClasses} bg-green-600 text-white flex items-center justify-center text-xs font-bold`}
          >
            AMEX
          </div>
        );
      default:
        return <CreditCardIcon className="w-8 h-8 text-gray-400" />;
    }
  };

  const totalSpent = transactions
    .filter((t) => t.type === "payment" && t.status === "completed")
    .reduce((sum, t) => sum + t.amount, 0);

  const pendingAmount = transactions
    .filter((t) => t.status === "pending")
    .reduce((sum, t) => sum + t.amount, 0);

  const tabs = [
    { id: "overview", name: "Overview" },
    { id: "methods", name: "Payment Methods" },
    { id: "transactions", name: "Transactions" },
    { id: "invoices", name: "Invoices" },
  ];

  return (
    <div className="max-w-7xl mx-auto">
      {/* Apple-style Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-light text-gray-900 tracking-tight">
          Payments
        </h1>
        <p className="text-lg text-gray-500 mt-3 font-light">
          Manage payment methods and view transaction history
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="mb-8">
        <div className="flex space-x-1 bg-gray-100 rounded-2xl p-1 w-fit">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
                activeTab === tab.id
                  ? "bg-white text-blue-600 shadow-sm"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {tab.name}
            </button>
          ))}
        </div>
      </div>

      {/* Overview Tab */}
      {activeTab === "overview" && (
        <div className="space-y-8">
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-green-100 rounded-2xl flex items-center justify-center">
                  <BanknotesIcon className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Spent</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {formatPrice(totalSpent, "USD")}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-yellow-100 rounded-2xl flex items-center justify-center">
                  <ClockIcon className="w-6 h-6 text-yellow-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Pending Payments</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {formatPrice(pendingAmount, "USD")}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center">
                  <CreditCardIcon className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Payment Methods</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {paymentMethods.length}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Transactions */}
          <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-medium text-gray-900">
                Recent Transactions
              </h2>
              <button
                onClick={() => setActiveTab("transactions")}
                className="text-blue-600 hover:text-blue-700 font-medium text-sm"
              >
                View All →
              </button>
            </div>

            <div className="space-y-4">
              {transactions.slice(0, 5).map((transaction) => (
                <div
                  key={transaction.id}
                  className="flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-2xl flex items-center justify-center ${
                        transaction.type === "payment"
                          ? "bg-blue-100"
                          : transaction.type === "refund"
                          ? "bg-green-100"
                          : "bg-gray-100"
                      }`}
                    >
                      {transaction.type === "payment" ? (
                        <CreditCardIcon className="w-4 h-4 text-blue-600" />
                      ) : transaction.type === "refund" ? (
                        <ArrowDownTrayIcon className="w-4 h-4 text-green-600" />
                      ) : (
                        <DocumentTextIcon className="w-4 h-4 text-gray-600" />
                      )}
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">
                        {transaction.description}
                      </p>
                      <p className="text-sm text-gray-500">
                        {formatDate(transaction.date)} •{" "}
                        {transaction.paymentMethod}
                      </p>
                    </div>
                  </div>

                  <div className="text-right">
                    <p
                      className={`font-semibold ${
                        transaction.type === "refund"
                          ? "text-green-600"
                          : "text-gray-900"
                      }`}
                    >
                      {transaction.type === "refund" ? "+" : "-"}
                      {formatPrice(transaction.amount, transaction.currency)}
                    </p>
                    <span
                      className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                        statusConfig[transaction.status].color
                      }`}
                    >
                      {statusConfig[transaction.status].label}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Payment Methods Tab */}
      {activeTab === "methods" && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-medium text-gray-900">
              Payment Methods
            </h2>
            <button className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-2xl font-medium transition-colors flex items-center gap-2">
              <PlusIcon className="w-4 h-4" />
              Add Payment Method
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {paymentMethods.map((method) => (
              <div
                key={method.id}
                className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6 relative"
              >
                {method.isDefault && (
                  <div className="absolute top-4 right-4">
                    <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">
                      Default
                    </span>
                  </div>
                )}

                <div className="flex items-center gap-4 mb-4">
                  {method.type === "paypal" ? (
                    <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center">
                      <span className="text-white font-bold text-sm">PP</span>
                    </div>
                  ) : (
                    <div className="w-12 h-12 bg-gray-100 rounded-2xl flex items-center justify-center">
                      {getBrandIcon(method.brand)}
                    </div>
                  )}
                  <div>
                    <h3 className="font-medium text-gray-900">
                      {method.type === "paypal"
                        ? "PayPal"
                        : `${method.brand.toUpperCase()} Card`}
                    </h3>
                    <p className="text-sm text-gray-600">{method.cardNumber}</p>
                  </div>
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Cardholder</span>
                    <span className="text-gray-900">{method.cardHolder}</span>
                  </div>
                  {method.expiryDate && (
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Expires</span>
                      <span className="text-gray-900">{method.expiryDate}</span>
                    </div>
                  )}
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Status</span>
                    <span
                      className={`font-medium ${
                        method.isActive ? "text-green-600" : "text-red-600"
                      }`}
                    >
                      {method.isActive ? "Active" : "Inactive"}
                    </span>
                  </div>
                </div>

                <div className="flex gap-2">
                  <button className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 rounded-2xl font-medium transition-colors text-sm flex items-center justify-center gap-2">
                    <PencilIcon className="w-4 h-4" />
                    Edit
                  </button>
                  {!method.isDefault && (
                    <button className="flex-1 bg-red-100 hover:bg-red-200 text-red-700 py-2 rounded-2xl font-medium transition-colors text-sm flex items-center justify-center gap-2">
                      <TrashIcon className="w-4 h-4" />
                      Remove
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Security Information */}
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-3xl p-6">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center flex-shrink-0">
                <ShieldCheckIcon className="w-6 h-6 text-blue-600" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-medium text-blue-900 mb-2">
                  Your Payment Information is Secure
                </h3>
                <p className="text-blue-700 mb-4">
                  We use industry-standard encryption to protect your payment
                  information. Your card details are tokenized and never stored
                  on our servers.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex items-center gap-2">
                    <CheckCircleIcon className="w-4 h-4 text-green-600" />
                    <span className="text-sm text-blue-800">
                      256-bit SSL Encryption
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircleIcon className="w-4 h-4 text-green-600" />
                    <span className="text-sm text-blue-800">
                      PCI DSS Compliant
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Transactions Tab */}
      {activeTab === "transactions" && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-medium text-gray-900">
              Transaction History
            </h2>
            <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors">
              <ArrowDownTrayIcon className="w-4 h-4" />
              Export
            </button>
          </div>

          {/* Filters */}
          <div className="flex flex-wrap items-center gap-4">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search transactions..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <select
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Time</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 3 months</option>
              <option value="365">Last year</option>
            </select>
          </div>

          {/* Transactions List */}
          <div className="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-900">
                      Transaction
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-900">
                      Date
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-900">
                      Amount
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-900">
                      Status
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-900">
                      Payment Method
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {transactions.map((transaction) => (
                    <tr key={transaction.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div
                            className={`w-8 h-8 rounded-2xl flex items-center justify-center ${
                              transaction.type === "payment"
                                ? "bg-blue-100"
                                : transaction.type === "refund"
                                ? "bg-green-100"
                                : "bg-gray-100"
                            }`}
                          >
                            {transaction.type === "payment" ? (
                              <CreditCardIcon className="w-4 h-4 text-blue-600" />
                            ) : transaction.type === "refund" ? (
                              <ArrowDownTrayIcon className="w-4 h-4 text-green-600" />
                            ) : (
                              <DocumentTextIcon className="w-4 h-4 text-gray-600" />
                            )}
                          </div>
                          <div>
                            <p className="font-medium text-gray-900">
                              {transaction.description}
                            </p>
                            {transaction.bookingReference && (
                              <p className="text-sm text-gray-500">
                                Ref: {transaction.bookingReference}
                              </p>
                            )}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {formatDate(transaction.date)}
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`font-semibold ${
                            transaction.type === "refund"
                              ? "text-green-600"
                              : "text-gray-900"
                          }`}
                        >
                          {transaction.type === "refund" ? "+" : "-"}
                          {formatPrice(
                            transaction.amount,
                            transaction.currency
                          )}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                            statusConfig[transaction.status].color
                          }`}
                        >
                          {statusConfig[transaction.status].label}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {transaction.paymentMethod}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Invoices Tab */}
      {activeTab === "invoices" && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-medium text-gray-900">Invoices</h2>
            <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors">
              <ArrowDownTrayIcon className="w-4 h-4" />
              Download All
            </button>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {invoices.map((invoice) => (
              <div
                key={invoice.id}
                className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-purple-100 rounded-2xl flex items-center justify-center">
                      <DocumentTextIcon className="w-6 h-6 text-purple-600" />
                    </div>
                    <div>
                      <h3 className="font-medium text-gray-900">
                        {invoice.invoiceNumber}
                      </h3>
                      <p className="text-sm text-gray-600">
                        {invoice.description}
                      </p>
                      <p className="text-xs text-gray-500">
                        Issued: {formatDate(invoice.date)} • Due:{" "}
                        {formatDate(invoice.dueDate)}
                      </p>
                    </div>
                  </div>

                  <div className="text-right">
                    <p className="text-xl font-semibold text-gray-900">
                      {formatPrice(invoice.amount, invoice.currency)}
                    </p>
                    <span
                      className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                        statusConfig[invoice.status].color
                      }`}
                    >
                      {statusConfig[invoice.status].label}
                    </span>
                  </div>
                </div>

                <div className="flex gap-2 mt-4">
                  <button className="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-2xl font-medium transition-colors text-sm">
                    <ArrowDownTrayIcon className="w-4 h-4" />
                    Download PDF
                  </button>
                  {invoice.status === "pending" && (
                    <button className="flex items-center gap-2 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-2xl font-medium transition-colors text-sm">
                      <CreditCardIcon className="w-4 h-4" />
                      Pay Now
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
