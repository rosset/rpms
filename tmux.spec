%global _hardened_build 1

Name:           tmux
Version:        3.1
Release:        1%{?dist}
Summary:        A terminal multiplexer

# Most of the source is ISC licensed; some of the files in compat/ are 2 and
# 3 clause BSD licensed.
License:        ISC and BSD
URL:            https://tmux.github.io/
Source0:        https://github.com/tmux/%{name}/releases/download/%{version}/%{name}-%{version}-rc4.tar.gz
# Examples has been removed - so include the bash_completion here
Source1:        bash_completion_tmux.sh
#Patch0:         749f67b7d801eed03345fef9c04206fbd079c3cb.patch
# Patch0 from https://github.com/tmux/tmux/commit/749f67b7d801eed03345fef9c04206fbd079c3cb.patch
# From 749f67b7d801eed03345fef9c04206fbd079c3cb Mon Sep 17 00:00:00 2001
# From: nicm <nicm>
# Date: Mon, 19 Nov 2018 13:35:40 +0000
# Subject: [PATCH] evbuffer_new and bufferevent_new can both fail (when malloc
# fails) and return NULL. GitHub issue 1547.


BuildRequires:  gcc
BuildRequires:  ncurses-devel
BuildRequires:  libevent-devel
BuildRequires:  libutempter-devel

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

%prep
%autosetup -n tmux-3.1-rc4

%build
%configure
%make_build


%install
%make_install
# bash completion
install -Dpm 644 %{SOURCE1} %{buildroot}%{_datadir}/bash-completion/completions/tmux

%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    touch %{_sysconfdir}/shells
  fi
  for binpath in %{_bindir} /bin; do
    if ! grep -q "^${binpath}/tmux$" %{_sysconfdir}/shells; then
       (cat %{_sysconfdir}/shells; echo "$binpath/tmux") > %{_sysconfdir}/shells.new
       mv %{_sysconfdir}/shells{.new,}
    fi
  done
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -e '\!^%{_bindir}/tmux$!d' -e '\!^/bin/tmux$!d' < %{_sysconfdir}/shells > %{_sysconfdir}/shells.new
  mv %{_sysconfdir}/shells{.new,}
fi

%files
%doc CHANGES
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*
%{_datadir}/bash-completion/completions/tmux

%changelog
* Sat Apr 11 2020 Filipe Rosset <rosset.filipe@gmail.com> - 3.1rc4-1
- 3.1rc4
