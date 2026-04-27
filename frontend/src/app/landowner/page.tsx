"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";

interface Notification {
  id: string;
  type: string;
  title: string;
  message: string;
  created_at: string;
  read: boolean;
  data?: any;
}

export default function LandownerDashboard() {
  const router = useRouter();
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading) {
      if (!isAuthenticated || !user) {
        router.push("/login");
        return;
      }
      loadData();
    }
  }, [authLoading, isAuthenticated, user]);

  const loadData = async () => {
    if (!user?.id) {
      return;
    }

    try {

      // Fetch notifications
      const notifResponse = await fetch(
<<<<<<< HEAD
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/notifications?user_id=${user.id}`
=======
        `/api/notifications?user_id=${user.id}`
>>>>>>> da550345cc51c621932513e1e9514dc23123e850
      );
      if (notifResponse.ok) {
        const data = await notifResponse.json();
        setNotifications(data.notifications || []);
      }
    } catch (error) {
      console.error("Error loading dashboard:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleNotificationClick = (notification: Notification) => {
    if (notification.type === "scan_complete") {
      router.push("/landowner/pending-scans");
    }
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8 flex items-center justify-center">
        <div className="text-gray-600">Loading dashboard...</div>
      </div>
    );
  }

  const unreadNotifications = notifications.filter(n => !n.read);
  const scanNotifications = notifications.filter(n => n.type === "scan_complete");

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome, {user?.full_name || "Landowner"}
          </h1>
          <p className="text-gray-600">
            Manage your land registrations and carbon credit approvals
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Pending Approvals</p>
                <p className="text-3xl font-bold text-yellow-600">
                  {scanNotifications.length}
                </p>
              </div>
              <div className="text-4xl">⏳</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Notifications</p>
                <p className="text-3xl font-bold text-blue-600">
                  {unreadNotifications.length}
                </p>
              </div>
              <div className="text-4xl">🔔</div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Quick Action</p>
                <Link
                  href="/request-registration"
                  className="text-sm text-terra-600 hover:text-terra-700 font-semibold"
                >
                  Register New Land →
                </Link>
              </div>
              <div className="text-4xl">🌳</div>
            </div>
          </div>
        </div>

        {/* Notifications Section */}
        {notifications.length > 0 && (
          <div className="bg-white rounded-lg shadow-md mb-8">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">Recent Notifications</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {notifications.slice(0, 5).map((notification) => (
                <div
                  key={notification.id}
                  onClick={() => handleNotificationClick(notification)}
                  className={`p-6 hover:bg-gray-50 cursor-pointer transition-colors ${
                    !notification.read ? "bg-blue-50" : ""
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <h3 className="font-semibold text-gray-900">
                          {notification.title}
                        </h3>
                        {!notification.read && (
                          <span className="inline-block w-2 h-2 bg-blue-600 rounded-full"></span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 mb-2">
                        {notification.message}
                      </p>
                      <p className="text-xs text-gray-400">
                        {new Date(notification.created_at).toLocaleString()}
                      </p>
                    </div>
                    {notification.type === "scan_complete" && (
                      <button className="ml-4 px-4 py-2 bg-terra-600 text-white text-sm font-semibold rounded-lg hover:bg-terra-700 transition-colors">
                        Review →
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action Items */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <Link
              href="/landowner/pending-scans"
              className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg hover:border-terra-500 hover:bg-terra-50 transition-all"
            >
              <div>
                <h3 className="font-semibold text-gray-900">Review Pending Scans</h3>
                <p className="text-sm text-gray-600 mt-1">
                  Approve or reject land scan results
                </p>
              </div>
              <div className="text-2xl">📊</div>
            </Link>

            <Link
              href="/request-registration"
              className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg hover:border-terra-500 hover:bg-terra-50 transition-all"
            >
              <div>
                <h3 className="font-semibold text-gray-900">Register New Land</h3>
                <p className="text-sm text-gray-600 mt-1">
                  Submit a new land registration request
                </p>
              </div>
              <div className="text-2xl">🗺️</div>
            </Link>

            <Link
              href="/marketplace"
              className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg hover:border-terra-500 hover:bg-terra-50 transition-all"
            >
              <div>
                <h3 className="font-semibold text-gray-900">View Marketplace</h3>
                <p className="text-sm text-gray-600 mt-1">
                  See your listed carbon credits
                </p>
              </div>
              <div className="text-2xl">💰</div>
            </Link>

            <Link
              href="/dashboard"
              className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg hover:border-terra-500 hover:bg-terra-50 transition-all"
            >
              <div>
                <h3 className="font-semibold text-gray-900">My Portfolio</h3>
                <p className="text-sm text-gray-600 mt-1">
                  View all your carbon credits
                </p>
              </div>
              <div className="text-2xl">📈</div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
