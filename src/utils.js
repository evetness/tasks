export function formatCurrency(amount, currency) {
  const formatter = new Intl.NumberFormat('hu-HU', {
    style: 'currency',
    currency: currency,
  });
  return formatter.format(amount)
}

export function sortByDate(a, b, field) {
  let da = new Date(a[field]), db = new Date(b[field]);
  return db - da;
}

export function sortByString(a, b, field) {
  let fa = a[field].toLowerCase(), fb = b[field].toLowerCase();

  if (fa < fb) return -1;
  if (fa > fb) return 1;

  return 0;
}