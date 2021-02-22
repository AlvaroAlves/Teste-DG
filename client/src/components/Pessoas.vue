<template>
  <div class="container">
    <div class="row">
      <div class="col-lg-10 mx-auto mb-4">
        <div class="section-title text-center ">
            <h3 class="top-c-sep">Cadastro de pessoas</h3>
            <p>Cadastro simples de pessoa.</p>
        </div>
        <alert :message="message" :variant="variant" v-if="showMessage"></alert>
      </div>
    </div>

    <div class="row"  v-for="(pessoa, index) in pessoas" :key="index">
      <div class="col-lg-10 mx-auto">
        <div class="career-search mb-60">
          <div class="filter-result">
            <div class="job-box d-md-flex align-items-center justify-content-between mb-30">
                <div class="job-left my-8 d-md-flex align-items-center flex-wrap">
                    <div
                    class="img-holder mr-md-4 mb-md-0 mb-4 mx-auto mx-md-0 d-md-none d-lg-flex">
                        FD
                    </div>
                    <div class="job-content">
                        <h5 class="text-center text-md-left">{{pessoa.nome}}</h5>
                        <ul class="d-md-flex flex-wrap text-capitalize ff-open-sans">
                            <li class="mr-md-4">
                                <i class="zmdi zmdi-pin mr-2"></i> Idade:
                            </li>
                            <li class="mr-md-4">
                                <i class="zmdi zmdi-pin mr-2"></i> {{pessoa.idade}} Anos
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="job-right my-4 flex-shrink-0">
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-warning btn-sm"
                            v-b-modal.pessoa-update-modal
                            @click="editPessoa(pessoa)">Atualizar</button>
                    <button type="button" class="btn btn-danger btn-sm"
                            @click="onDeletePessoa(pessoa)">Deletar</button>
                  </div>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-10 mx-auto">
        <button type="button" class="btn btn-success btn-sm"
                v-b-modal.pessoa-modal>Adicionar Registro</button>
        <br>
      </div>
    </div>
    <b-modal ref="addPessoasModal" id="pessoa-modal" title="Inclua um novo registro" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-nome-group" label="Nome:" label-for="form-nome-input">
          <b-form-input id="form-nome-input"
                        type="text"
                        v-model="addPessoasForm.nome"
                        required
                        placeholder="Digite o nome"></b-form-input>
        </b-form-group>
        <b-form-group id="form-datanascimento-group"
                      label="Data de Nascimento:"
                      label-for="form-datanascimento-input">
          <b-form-input id="form-datanascimento-input"
                        type="date"
                        v-model="addPessoasForm.nascimento"
                        required
                        placeholder="Data de Nascimento: DD/MM/AAAA"></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Confirmar</b-button>
        <b-button type="reset" variant="danger">Limpar</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editPessoaModal"
        id="pessoa-update-modal"
        title="Update"
        hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-nome-edit-group"
                    label="Nome:"
                    label-for="form-nome-edit-input">
          <b-form-input id="form-nome-edit-input"
                        type="text"
                        v-model="editForm.nome"
                        required
                        placeholder="Digite o Nome:">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-nascimento-edit-group"
                      label="Data de nascimento:"
                      label-for="form-nascimento-edit-input">
          <b-form-input id="form-nascimento-edit-input"
                          type="date"
                          v-model="editForm.nascimento"
                          required>
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Atualizar</b-button>
          <b-button type="reset" variant="danger">Cancelar</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      pessoas: [],
      addPessoasForm: {
        nome: '',
        nascimento: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        nome: '',
        nascimento: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getPessoas() {
      const path = 'http://localhost:5000/pessoas';
      axios.get(path)
        .then((res) => {
          this.pessoas = res.data.pessoas;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addPessoas(payLoad) {
      const path = 'http://localhost:5000/pessoas';
      axios.post(path, payLoad)
        .then(() => {
          this.getPessoas();
          this.message = 'Pessoa cadastrada com sucesso!';
          this.variant = 'success';
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
          this.getPessoas();
        });
    },
    updatePessoa(payLoad, pessoaID) {
      const path = `http://localhost:5000/pessoas/${pessoaID}`;
      axios.put(path, payLoad)
        .then(() => {
          this.getPessoas();
          this.message = 'Dados de pessoa atualizados!';
          this.variant = 'success';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getPessoas();
        });
    },
    removePessoa(pessoaID) {
      const path = `http://localhost:5000/pessoas/${pessoaID}`;
      axios.delete(path)
        .then(() => {
          this.getPessoas();
          this.message = 'Pessoa Excluída!';
          this.variant = 'success';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getPessoas();
        });
    },
    editPessoa(pessoa) {
      this.editForm = pessoa;
    },
    initForm() {
      this.addPessoasForm.nome = '';
      this.addPessoasForm.nascimento = '';
      this.editForm.id = '';
      this.editForm.nome = '';
      this.editForm.nascimento = '';
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editPessoaModal.hide();
      if (new Date().setHours(0, 0, 0, 0) < new Date(this.addPessoasForm.nascimento)) {
        this.message = 'Data de nascimento inválida!';
        this.variant = 'danger';
        this.showMessage = true;
        this.initForm();
        return;
      }
      const payLoad = {
        nome: this.editForm.nome,
        nascimento: this.editForm.nascimento,
      };
      this.updatePessoa(payLoad, this.editForm.id);
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addPessoasModal.hide();
      if (new Date().setHours(0, 0, 0, 0) < new Date(this.addPessoasForm.nascimento)) {
        this.message = 'Data de nascimento inválida!';
        this.variant = 'danger';
        this.showMessage = true;
        this.initForm();
        return;
      }
      const payLoad = {
        nome: this.addPessoasForm.nome,
        nascimento: this.addPessoasForm.nascimento,
      };
      this.addPessoas(payLoad);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addPessoasModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.editPessoaModal.hide();
      this.initForm();
      this.getPessoas();
    },
    onDeletePessoa(pessoa) {
      this.removePessoa(pessoa.id);
    },
  },
  created() {
    this.getPessoas();
  },
};
</script>

<style scoped>
/* baseado no snippet = https://bootsnipp.com/snippets/6AOlK */
  body{
    background:#f5f5f5;
    margin-top:20px;}

/* ===== Career ===== */
.career-form {
  background-color: #4e63d7;
  border-radius: 5px;
  padding: 0 16px;
}

.career-form .form-control {
  background-color: rgba(255, 255, 255, 0.2);
  border: 0;
  padding: 12px 15px;
  color: #fff;
}

.career-form .form-control::-webkit-input-placeholder {
  /* Chrome/Opera/Safari */
  color: #fff;
}

.career-form .form-control::-moz-placeholder {
  /* Firefox 19+ */
  color: #fff;
}

.career-form .form-control:-ms-input-placeholder {
  /* IE 10+ */
  color: #fff;
}

.career-form .form-control:-moz-placeholder {
  /* Firefox 18- */
  color: #fff;
}

.career-form .custom-select {
  background-color: rgba(255, 255, 255, 0.2);
  border: 0;
  padding: 12px 15px;
  color: #fff;
  width: 100%;
  border-radius: 5px;
  text-align: left;
  height: auto;
  background-image: none;
}

.filter-result .job-box {
  -webkit-box-shadow: 0 0 35px 0 rgba(130, 130, 130, 0.2);
          box-shadow: 0 0 35px 0 rgba(130, 130, 130, 0.2);
  border-radius: 10px;
  padding: 10px 35px;
}

ul {
  list-style: none;
}

.list-disk li {
  list-style: none;
  margin-bottom: 12px;
}

.list-disk li:last-child {
  margin-bottom: 0;
}

.job-box .img-holder {
  height: 65px;
  width: 65px;
  background-color: #4e63d7;
  background-image: -webkit-gradient(linear, left top, right top,
  from(rgba(78, 99, 215, 0.9)), to(#5a85dd));
  background-image:
  linear-gradient(to right, rgba(78, 99, 215, 0.9) 0%, #5a85dd 100%);
  font-family: "Open Sans", sans-serif;
  color: #fff;
  font-size: 22px;
  font-weight: 700;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: center;
      -ms-flex-pack: center;
          justify-content: center;
  -webkit-box-align: center;
      -ms-flex-align: center;
          align-items: center;
  border-radius: 65px;
}

.career-title {
  background-color: #4e63d7;
  color: #fff;
  padding: 15px;
  text-align: center;
  border-radius: 10px 10px 0 0;
  background-image: -webkit-gradient(linear, left top, right top,
  from(rgba(78, 99, 215, 0.9)), to(#5a85dd));
  background-image: linear-gradient(to right, rgba(78, 99, 215, 0.9) 0%, #5a85dd 100%);
}

.job-overview {
  -webkit-box-shadow: 0 0 35px 0 rgba(130, 130, 130, 0.2);
          box-shadow: 0 0 35px 0 rgba(130, 130, 130, 0.2);
  border-radius: 10px;
}

@media (min-width: 992px) {
  .job-overview {
    position: -webkit-sticky;
    position: sticky;
    top: 70px;
  }
}

.job-overview .job-detail ul {
  margin-bottom: 28px;
}

.job-overview .job-detail ul li {
  opacity: 0.75;
  font-weight: 600;
  margin-bottom: 15px;
}

.job-overview .job-detail ul li i {
  font-size: 20px;
  position: relative;
  top: 1px;
}

.job-overview .overview-bottom,
.job-overview .overview-top {
  padding: 35px;
}

.job-content ul li {
  font-weight: 600;
  opacity: 0.75;
  border-bottom: 1px solid #ccc;
  padding: 10px 5px;
}

@media (min-width: 768px) {
  .job-content ul li {
    border-bottom: 0;
    padding: 0;
  }
}

.job-content ul li i {
  font-size: 20px;
  position: relative;
  top: 1px;
}
.mb-30 {
    margin-bottom: 30px;
}
</style>
