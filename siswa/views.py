from django.shortcuts import render, redirect
from django.db import connection


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# =========================
# LIST SISWA
# =========================
def siswa_list(request):

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT id, nama, umur, tgl_lahir, status_hadir, nilai_akhir
            FROM siswa
            ORDER BY id DESC
        """)

        data_siswa = dictfetchall(cursor)

    context = {
        'keyword': 'bandung',
        'data': data_siswa
    }

    return render(request, 'list.html', context)


# =========================
# DETAIL SISWA
# =========================
def siswa_detail(request, id):

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT id, nama, umur, tgl_lahir, status_hadir, nilai_akhir
            FROM siswa
            WHERE id = %s
        """, [id])

        siswa = dictfetchall(cursor)

    context = {
        'siswa': siswa[0] if siswa else None
    }

    return render(request, 'detail.html', context)


# =========================
# TAMBAH SISWA
# =========================
def siswa_create(request):

    if request.method == 'POST':

        nama = request.POST.get('nama')
        umur = request.POST.get('umur')
        tgl_lahir = request.POST.get('tgl_lahir')
        status_hadir = request.POST.get('status_hadir')
        nilai_akhir = request.POST.get('nilai_akhir')

        with connection.cursor() as cursor:

            cursor.execute("""
                INSERT INTO siswa
                (nama, umur, tgl_lahir, status_hadir, nilai_akhir)
                VALUES (%s, %s, %s, %s, %s)
            """, [
                nama,
                umur,
                tgl_lahir,
                status_hadir == 'True',
                nilai_akhir
            ])

        return redirect('siswa_list')

    return render(request, 'create.html')


# =========================
# EDIT SISWA
# =========================
def siswa_update(request, id):

    with connection.cursor() as cursor:

        if request.method == 'POST':

            nama = request.POST.get('nama')
            umur = request.POST.get('umur')
            tgl_lahir = request.POST.get('tgl_lahir')
            status_hadir = request.POST.get('status_hadir')
            nilai_akhir = request.POST.get('nilai_akhir')

            cursor.execute("""
                UPDATE siswa
                SET
                    nama = %s,
                    umur = %s,
                    tgl_lahir = %s,
                    status_hadir = %s,
                    nilai_akhir = %s
                WHERE id = %s
            """, [
                nama,
                umur,
                tgl_lahir,
                status_hadir == 'True',
                nilai_akhir,
                id
            ])

            return redirect('siswa_list')

        cursor.execute("""
            SELECT id, nama, umur, tgl_lahir, status_hadir, nilai_akhir
            FROM siswa
            WHERE id = %s
        """, [id])

        siswa = dictfetchall(cursor)

    context = {
        'siswa': siswa[0] if siswa else None
    }

    return render(request, 'edit.html', context)


# =========================
# HAPUS SISWA
# =========================
def siswa_delete(request, id):

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT id, nama, umur, tgl_lahir, status_hadir, nilai_akhir
            FROM siswa
            WHERE id = %s
        """, [id])

        siswa = dictfetchall(cursor)

        if request.method == 'POST':

            cursor.execute("""
                DELETE FROM siswa
                WHERE id = %s
            """, [id])

            return redirect('siswa_list')

    context = {
        'siswa': siswa[0] if siswa else None
    }

    return render(request, 'delete.html', context)