export function getUserName(email) {
  const userName = email.split('@')[0];
  return userName;
}
