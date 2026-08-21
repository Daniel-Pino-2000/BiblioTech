import { useState } from "react";
import type { FormEvent } from "react";
import { useAuth } from "../context/AuthContext";
import * as authApi from "../api/auth";
import { ApiError } from "../api/client";

export function ProfilePage() {
  const { user, refreshUser } = useAuth();
  const [name, setName] = useState(user?.name || "");
  const [address, setAddress] = useState(user?.address || "");
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  if (!user) return null;

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!user) return;
    setStatus(null);
    setError(null);
    try {
      await authApi.updateProfile(user.username, { name, address });
      await refreshUser();
      setStatus("Profile updated.");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to update profile");
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Your profile</h1>
      </div>

      <div className="profile-card">
        <div className="profile-row">
          <span className="profile-label">Username</span>
          <span>{user.username}</span>
        </div>
        <div className="profile-row">
          <span className="profile-label">Email</span>
          <span>{user.email || "—"}</span>
        </div>
      </div>

      <form className="auth-card profile-form" onSubmit={handleSubmit}>
        <h2>Edit details</h2>

        <label>
          Name
          <input value={name} onChange={(e) => setName(e.target.value)} />
        </label>

        <label>
          Address
          <input value={address} onChange={(e) => setAddress(e.target.value)} />
        </label>

        {status && <div className="form-success">{status}</div>}
        {error && <div className="form-error">{error}</div>}

        <button className="btn btn-primary" type="submit">
          Save changes
        </button>
      </form>
    </div>
  );
}
